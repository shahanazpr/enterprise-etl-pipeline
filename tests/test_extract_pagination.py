from unittest.mock import patch, MagicMock, mock_open
from requests.exceptions import HTTPError

from extract.extract_api import fetch_all_pages, extract_data


# ---------------------------------------------------------------------------
# 1. Pagination — verifies that fetch_all_pages() walks through multiple
#    pages and aggregates ALL records, not just the first page.
# ---------------------------------------------------------------------------
@patch("extract.extract_api.requests.get")
def test_fetch_all_pages_aggregates_multiple_pages(mock_get):
    page1 = MagicMock(status_code=200)
    page1.json.return_value = [{"id": 1}, {"id": 2}, {"id": 3}]
    page1.raise_for_status.return_value = None

    page2 = MagicMock(status_code=200)
    page2.json.return_value = [{"id": 4}, {"id": 5}]  # partial page -> last page
    page2.raise_for_status.return_value = None

    mock_get.side_effect = [page1, page2]

    records = fetch_all_pages("http://fake-api/users", page_limit=3)

    assert len(records) == 5
    assert [r["id"] for r in records] == [1, 2, 3, 4, 5]
    assert mock_get.call_count == 2

    # Confirm it actually requested page 1 then page 2 with the right params
    first_call_params = mock_get.call_args_list[0].kwargs["params"]
    second_call_params = mock_get.call_args_list[1].kwargs["params"]
    assert first_call_params == {"_page": 1, "_limit": 3}
    assert second_call_params == {"_page": 2, "_limit": 3}


@patch("extract.extract_api.requests.get")
def test_fetch_all_pages_stops_on_empty_page(mock_get):
    page1 = MagicMock(status_code=200)
    page1.json.return_value = [{"id": 1}, {"id": 2}, {"id": 3}]
    page1.raise_for_status.return_value = None

    page2 = MagicMock(status_code=200)
    page2.json.return_value = [{"id": 4}, {"id": 5}, {"id": 6}]  # full page again
    page2.raise_for_status.return_value = None

    page3 = MagicMock(status_code=200)
    page3.json.return_value = []  # explicitly empty -> stop
    page3.raise_for_status.return_value = None

    mock_get.side_effect = [page1, page2, page3]

    records = fetch_all_pages("http://fake-api/users", page_limit=3)

    assert len(records) == 6
    assert mock_get.call_count == 3


@patch("extract.extract_api.requests.get")
def test_fetch_all_pages_detects_endpoint_that_ignores_pagination(mock_get):
    """
    Some APIs (as discovered while building this) silently ignore unknown
    _page/_limit query params and just return the full dataset every time.
    fetch_all_pages() must detect this (identical record IDs on consecutive
    "pages") and stop, instead of looping forever or duplicating records.
    """
    same_page = MagicMock(status_code=200)
    same_page.json.return_value = [{"id": i} for i in range(1, 11)]  # always 10 records
    same_page.raise_for_status.return_value = None

    # Every call returns the exact same 10 records, as if pagination is ignored
    mock_get.side_effect = [same_page, same_page, same_page]

    records = fetch_all_pages("http://fake-api/users", page_limit=3, max_pages=10)

    # Should stop after the 2nd call once it notices page 2 == page 1
    assert len(records) == 10
    assert mock_get.call_count == 2


@patch("extract.extract_api.requests.get")
def test_fetch_all_pages_respects_max_pages_safety_cap(mock_get):
    """If nothing ever signals completion, the hard cap must still stop it."""
    growing_page = MagicMock(status_code=200)
    # Always returns exactly page_limit records with NEW ids each time
    # (simulates a pathological API that never returns a partial/empty page)
    def make_response(ids):
        r = MagicMock(status_code=200)
        r.json.return_value = [{"id": i} for i in ids]
        r.raise_for_status.return_value = None
        return r

    mock_get.side_effect = [make_response(range(i, i + 3)) for i in range(0, 30, 3)]

    records = fetch_all_pages("http://fake-api/users", page_limit=3, max_pages=5)

    assert mock_get.call_count == 5
    assert len(records) == 15  # 5 pages * 3 records, then hard-stopped


# ---------------------------------------------------------------------------
# 2. Rate limiting + retry — verifies that a 429 response is logged and
#    causes a retry via the existing tenacity @retry decorator on
#    extract_data(), eventually succeeding once the API responds normally.
# ---------------------------------------------------------------------------
@patch("extract.extract_api.upload_to_s3")
@patch("extract.extract_api.json.dump")
@patch("extract.extract_api.open", new_callable=mock_open)
@patch("extract.extract_api.requests.get")
def test_extract_data_retries_after_rate_limit(
    mock_get, mock_file, mock_json_dump, mock_upload, monkeypatch
):
    rate_limited = MagicMock(status_code=429, headers={"Retry-After": "1"})
    rate_limited.raise_for_status.side_effect = HTTPError("429 Too Many Requests")

    success = MagicMock(status_code=200)
    success.raise_for_status.return_value = None
    success.json.return_value = [
        {
            "id": 1,
            "name": "Alice",
            "username": "alice123",
            "email": "alice@example.com",
            "phone": "123-456",
            "website": "alice.example.com",
            "address": {"city": "Springfield", "zipcode": "12345"},
            "company": {"name": "Acme Corp"},
        }
    ]

    # First call to the API is rate-limited (429), second call succeeds.
    # extract_data()'s own @retry decorator re-invokes fetch_all_pages
    # from scratch on failure, so both calls target "page 1".
    mock_get.side_effect = [rate_limited, success]

    extract_data()

    assert mock_get.call_count == 2
    mock_json_dump.assert_called_once()
