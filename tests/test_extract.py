import json
import os

from extract.extract_api import extract_data


class MockResponse:

    def raise_for_status(self):
        pass

    def json(self):
        return [
            {
                "id": 1,
                "name": "Testuser",
                "username": "user1",
                "email": "abc@gmail.com"
            }
        ]


def test_extract_data(monkeypatch):

    os.makedirs("data", exist_ok=True)

    monkeypatch.setenv("API_URL", "http://dummy")

    import requests

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())

    extract_data()

    with open("data/users.json") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["name"] == "Testuser"