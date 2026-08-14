"""
Enterprise ETL Pipeline - Live Dashboard
------------------------------------------
Reads REAL data from your PostgreSQL 'users' table and REAL run history
parsed from logs/etl_pipeline.log.

Place this file at the ROOT of your enterprise-etl-pipeline project
(same folder as main.py), then run:

    pip install streamlit pandas sqlalchemy psycopg2-binary python-dotenv
    streamlit run dashboard_app.py
"""

import os
import re
import subprocess
import sys
from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================================
# SETUP / CONFIG
# ============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Log file location
LOG_PATH = os.path.join(BASE_DIR, "logs", "etl_pipeline.log")


# Streamlit page configuration
st.set_page_config(
    page_title="Enterprise ETL Pipeline - Live Dashboard",
    page_icon="📊",
    layout="wide",
)


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


@st.cache_resource
def get_engine():
    """
    Create and cache the PostgreSQL SQLAlchemy engine.
    """

    url = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
    )

    return create_engine(url)


def fetch_warehouse_stats():
    """
    Pull the real row count and a preview of the users table
    directly from PostgreSQL.
    """

    try:
        engine = get_engine()

        with engine.connect() as conn:

            # Get total number of records
            count = conn.execute(
                text("SELECT COUNT(*) FROM users")
            ).scalar()

            # Get first 25 records
            preview = pd.read_sql(
                text(
                    "SELECT * FROM users "
                    "ORDER BY id "
                    "LIMIT 25"
                ),
                conn,
            )

        return count, preview, None

    except Exception as e:
        return None, None, str(e)


# ============================================================================
# LOG PARSING
# ============================================================================

LOG_LINE_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} "
    r"\d{2}:\d{2}:\d{2}) "
    r"\| (?P<level>\w+)\s*"
    r"\| (?P<logger>\S+) "
    r"\| (?P<msg>.*)$"
)

STAGE_DONE_RE = re.compile(
    r"Finished '(\w+)' in ([\d.]+)s"
)

STAGE_FAILED_RE = re.compile(
    r"'(\w+)' failed after ([\d.]+)s"
)

EXTRACTED_RE = re.compile(
    r"Successfully fetched (\d+) records"
)

VALID_RE = re.compile(
    r"Valid records: (\d+)"
)

SKIPPED_RE = re.compile(
    r"Skipped (\d+) invalid records|"
    r"(\d+) record\(s\) were skipped"
)

LOADED_RE = re.compile(
    r"Successfully loaded (\d+) records into PostgreSQL"
)


def parse_log_file(path):
    """
    Parse logs/etl_pipeline.log into a list of pipeline run summaries.

    Returns:
        runs
        parsed log entries
    """

    if not os.path.exists(path):
        return [], []

    # ------------------------------------------------------------------------
    # Read log file
    # ------------------------------------------------------------------------

    try:
        with open(path, "r", errors="ignore") as f:
            lines = f.readlines()

    except Exception:
        return [], []


    # ------------------------------------------------------------------------
    # Parse individual log lines
    # ------------------------------------------------------------------------

    parsed = []

    for line in lines:

        match = LOG_LINE_RE.match(line.strip())

        if match:
            parsed.append(match.groupdict())


    # ------------------------------------------------------------------------
    # Build pipeline runs
    # ------------------------------------------------------------------------

    runs = []

    current = None

    for entry in parsed:

        msg = entry["msg"]


        # --------------------------------------------------------------------
        # Detect beginning of a new pipeline run
        # --------------------------------------------------------------------

        if "Starting 'main'" in msg:

            current = {
                "start_time": entry["ts"],
                "status": "unknown",

                "total_s": None,

                "extract_s": None,
                "transform_s": None,
                "load_s": None,

                "extracted": None,
                "valid": None,
                "rejected": None,
                "loaded": None,

                "warnings": 0,
                "errors": 0,
            }

            runs.append(current)


        # Ignore entries before the first pipeline run
        if current is None:
            continue


        # --------------------------------------------------------------------
        # Count warnings and errors
        # --------------------------------------------------------------------

        if entry["level"] == "WARNING":
            current["warnings"] += 1

        if entry["level"] == "ERROR":
            current["errors"] += 1


        # --------------------------------------------------------------------
        # Successful stages
        # --------------------------------------------------------------------

        done = STAGE_DONE_RE.search(msg)

        if done:

            stage = done.group(1)
            seconds = float(done.group(2))

            if stage == "main":

                current["total_s"] = seconds
                current["status"] = "success"

            elif stage == "extract_data":

                current["extract_s"] = seconds

            elif stage == "transform_data":

                current["transform_s"] = seconds

            elif stage == "load_data":

                current["load_s"] = seconds


        # --------------------------------------------------------------------
        # Failed stages
        # --------------------------------------------------------------------

        failed = STAGE_FAILED_RE.search(msg)

        if failed:

            stage = failed.group(1)
            seconds = float(failed.group(2))

            if stage == "main":

                current["total_s"] = seconds
                current["status"] = "failed"


        # --------------------------------------------------------------------
        # Extracted records
        # --------------------------------------------------------------------

        extracted = EXTRACTED_RE.search(msg)

        if extracted:

            current["extracted"] = int(
                extracted.group(1)
            )


        # --------------------------------------------------------------------
        # Valid records
        # --------------------------------------------------------------------

        valid = VALID_RE.search(msg)

        if valid:

            current["valid"] = int(
                valid.group(1)
            )


        # --------------------------------------------------------------------
        # Rejected / skipped records
        # --------------------------------------------------------------------

        skipped = SKIPPED_RE.search(msg)

        if skipped:

            current["rejected"] = int(
                skipped.group(1)
                or skipped.group(2)
            )


        # --------------------------------------------------------------------
        # Loaded records
        # --------------------------------------------------------------------

        loaded = LOADED_RE.search(msg)

        if loaded:

            current["loaded"] = int(
                loaded.group(1)
            )


    # ------------------------------------------------------------------------
    # Remove incomplete runs where absolutely nothing was recorded
    # ------------------------------------------------------------------------

    runs = [
        r
        for r in runs
        if r["total_s"] is not None
        or r["status"] != "unknown"
    ]


    # Most recent run first
    runs.reverse()

    return runs, parsed


# ============================================================================
# PAGE HEADER
# ============================================================================

st.title("📊 Enterprise ETL Pipeline — Live Dashboard")

st.caption(
    "Zaalima Development · reads directly from your PostgreSQL "
    "database and log file"
)


# ============================================================================
# CONTROL BUTTONS
# ============================================================================

col_refresh, col_run, _ = st.columns([1, 1, 4])


# ---------------------------------------------------------------------------
# Refresh button
# ---------------------------------------------------------------------------

with col_refresh:

    if st.button("🔄 Refresh"):

        st.cache_resource.clear()

        st.rerun()


# ---------------------------------------------------------------------------
# Run pipeline button
# ---------------------------------------------------------------------------

with col_run:

    run_now = st.button("▶️ Run Pipeline Now")


# ============================================================================
# RUN PIPELINE
# ============================================================================

if run_now:

    with st.spinner(
        "Running main.py — this hits the real API and "
        "writes to your real database..."
    ):

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    os.path.join(BASE_DIR, "main.py"),
                ],
                capture_output=True,
                text=True,
                cwd=BASE_DIR,
            )

        except Exception as e:

            result = None

            st.error(
                f"Could not start the pipeline: {e}"
            )


    if result is not None:

        if result.returncode == 0:

            st.success(
                "Pipeline finished successfully. "
                "Click Refresh to see the new run."
            )

        else:

            st.error(
                "Pipeline failed. See output below."
            )


        with st.expander(
            "Show pipeline output"
        ):

            st.code(
                result.stdout
                + "\n"
                + result.stderr
            )


# ============================================================================
# SEPARATOR
# ============================================================================

st.divider()


# ============================================================================
# GET DATABASE AND LOG DATA
# ============================================================================

row_count, preview_df, db_error = fetch_warehouse_stats()

runs, all_log_entries = parse_log_file(LOG_PATH)


# ============================================================================
# KPI CARDS
# ============================================================================

k1, k2, k3, k4, k5 = st.columns(5)


# ---------------------------------------------------------------------------
# Warehouse row count
# ---------------------------------------------------------------------------

k1.metric(
    "Rows in warehouse",
    row_count
    if row_count is not None
    else "—"
)


# ---------------------------------------------------------------------------
# Pipeline statistics
# ---------------------------------------------------------------------------

if runs:

    # Number of successful runs
    success_count = sum(
        1
        for r in runs
        if r["status"] == "success"
    )


    # Success rate
    success_rate = round(
        100 * success_count / len(runs)
    )


    # Average duration
    durations = [
        r["total_s"]
        for r in runs
        if r["total_s"] is not None
    ]


    if durations:

        avg_duration = round(
            sum(durations) / len(durations),
            2
        )

    else:

        avg_duration = 0


    # Latest run
    last_run = runs[0]


    # Display KPIs
    k2.metric(
        "Runs found in log",
        len(runs)
    )

    k3.metric(
        "Success rate",
        f"{success_rate}%"
    )

    k4.metric(
        "Avg run duration",
        f"{avg_duration}s"
    )

    k5.metric(
        "Last run status",
        last_run["status"].capitalize()
    )


else:

    k2.metric(
        "Runs found in log",
        0
    )

    k3.metric(
        "Success rate",
        "—"
    )

    k4.metric(
        "Avg run duration",
        "—"
    )

    k5.metric(
        "Last run status",
        "—"
    )


# ============================================================================
# DATABASE ERROR
# ============================================================================

if db_error:

    st.error(
        f"Could not connect to PostgreSQL: {db_error}"
    )

    st.caption(
        "Check that PostgreSQL is running and .env has correct "
        "DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME."
    )


# ============================================================================
# NO RUN HISTORY
# ============================================================================

if not runs:

    st.warning(
        f"No completed pipeline runs found in {LOG_PATH}. "
        "Run `python main.py` at least once, or click "
        "'Run Pipeline Now' above."
    )


# ============================================================================
# CHARTS
# ============================================================================

st.divider()


if runs:

    # Use latest 15 runs
    df_runs = (
        pd.DataFrame(runs[:15])
        .iloc[::-1]
        .copy()
    )


    # Create chart labels
    df_runs["label"] = (
        df_runs["start_time"]
        .str[5:16]
    )


    # ========================================================================
    # STAGE DURATION CHART
    # ========================================================================

    left, right = st.columns([3, 2])


    with left:

        st.subheader(
            "Stage duration per run"
        )


        stage_df = (
            df_runs
            .set_index("label")[
                [
                    "extract_s",
                    "transform_s",
                    "load_s",
                ]
            ]
            .fillna(0)
        )


        stage_df.columns = [
            "Extract",
            "Transform",
            "Load",
        ]


        st.bar_chart(
            stage_df
        )


    # ========================================================================
    # VALIDATION OUTCOME
    # ========================================================================

    with right:

        st.subheader(
            "Validation outcome (all runs)"
        )


        total_valid = sum(
            r["valid"] or 0
            for r in runs
        )


        total_rejected = sum(
            r["rejected"] or 0
            for r in runs
        )


        outcome_df = pd.DataFrame(
            {
                "count": [
                    total_valid,
                    total_rejected,
                ]
            },
            index=[
                "Valid",
                "Rejected",
            ],
        )


        st.bar_chart(
            outcome_df
        )


        st.metric(
            "Total valid records extracted",
            total_valid
        )


        st.metric(
            "Total rejected records",
            total_rejected
        )


    # ========================================================================
    # WARNING / ERROR CHART
    # ========================================================================

    st.subheader(
        "Log level counts (WARNING / ERROR) per run"
    )


    log_level_df = (
        df_runs
        .set_index("label")[
            [
                "warnings",
                "errors",
            ]
        ]
    )


    log_level_df.columns = [
        "Warnings",
        "Errors",
    ]


    st.bar_chart(
        log_level_df
    )


# ============================================================================
# RECENT PIPELINE RUNS
# ============================================================================

st.divider()

st.subheader(
    "Recent pipeline runs (parsed from log file)"
)


if runs:

    table_df = pd.DataFrame(
        runs[:12]
    )


    table_df = table_df.rename(
        columns={
            "start_time": "Started",
            "status": "Status",

            "total_s": "Duration (s)",
            "extract_s": "Extract (s)",
            "transform_s": "Transform (s)",
            "load_s": "Load (s)",

            "extracted": "Extracted",
            "valid": "Valid",
            "rejected": "Rejected",
            "loaded": "Loaded to DB",

            "warnings": "Warnings",
            "errors": "Errors",
        }
    )


    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
    )


else:

    st.info(
        "No run history yet."
    )


# ============================================================================
# USERS TABLE PREVIEW
# ============================================================================

st.divider()

st.subheader(
    "users table preview (live from PostgreSQL)"
)


if preview_df is not None:

    st.dataframe(
        preview_df,
        use_container_width=True,
        hide_index=True,
    )


else:

    st.info(
        "Could not load table preview — "
        "check the database connection above."
    )


# ============================================================================
# RAW LOG TAIL
# ============================================================================

with st.expander(
    "Raw log tail (last 50 lines)"
):

    if all_log_entries:

        tail = all_log_entries[-50:]


        for entry in tail:

            level = entry["level"]


            color = {
                "INFO": "gray",
                "WARNING": "orange",
                "ERROR": "red",
            }.get(
                level,
                "gray"
            )


            st.markdown(
                f":{color}["
                f"{entry['ts']} | "
                f"{entry['level']:<8} | "
                f"{entry['msg']}"
                f"]"
            )

    else:

        st.write(
            "No log entries found."
        )


# ============================================================================
# FOOTER
# ============================================================================

st.caption(
    f"Log file: {LOG_PATH}"
)

st.caption(
    "Last refreshed: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)