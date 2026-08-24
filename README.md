Enterprise ETL Pipeline & Data Warehouse Synchronizer

Overview

This project is a production-style ETL (Extract, Transform, Load)
pipeline developed in Python as part of the Zaalima Development
Internship.

The pipeline extracts user data from an external REST API, validates the
records, transforms the data into a clean CSV format, and loads the
processed records into a PostgreSQL database using SQLAlchemy.

The project also includes AWS S3 integration for optional raw-data
storage, retry handling for S3 uploads, Apache Airflow orchestration,
Docker support, structured logging, email notifications, automated
testing with Pytest, and a Streamlit live monitoring dashboard.

Project Architecture

                        REST API
                           |
                           v
                    Data Extraction
                      (Requests)
                           |
                           v
                     Validation
                      (Pydantic)
                           |
                           +---------------> AWS S3
                           |                  Raw JSON
                           v
                     Transformation
                       (Pandas)
                           |
                           v
                        Loading
                 (SQLAlchemy + PostgreSQL)
                           |
                           v
                 Logging & Notifications
                           |
                           v
                   Apache Airflow
                           |
                           v
                  Streamlit Dashboard

------------------------------------------------------------------------

Features

-   Extract user data from REST APIs
-   Validate extracted data using Pydantic
-   Transform JSON data into CSV using Pandas
-   Load processed data into PostgreSQL
-   SQLAlchemy ORM integration
-   Upsert existing and new user records
-   Optional raw JSON storage in AWS S3
-   Date-based S3 object organization
-   Automatic retry handling for S3 uploads
-   Environment-based configuration using .env
-   Structured application logging
-   Email notification support
-   Apache Airflow DAG orchestration
-   Docker and Docker Compose support
-   Streamlit live monitoring dashboard
-   Pipeline run history and status monitoring
-   Stage-duration monitoring
-   Validation outcome monitoring
-   Warning and error monitoring
-   Pytest-based automated testing
-   Git and GitHub version control
-   GitHub Actions integration

------------------------------------------------------------------------

Tech Stack

-   Python 3.12+
-   Requests
-   Pandas
-   Pydantic
-   SQLAlchemy
-   PostgreSQL
-   AWS S3
-   Boto3
-   Tenacity
-   Apache Airflow
-   Streamlit
-   Docker / Docker Compose
-   Pytest
-   Git / GitHub
-   GitHub Actions

------------------------------------------------------------------------

Project Structure

    enterprise-etl-pipeline/
    |
    ├── dags/
    │   └── etl_pipeline.py
    |
    ├── data/
    │   ├── users.json
    │   └── users.csv
    |
    ├── database/
    │   └── connection.py
    |
    ├── extract/
    │   └── extract_api.py
    |
    ├── loading/
    │   └── upsert_users.py
    |
    ├── models/
    │   └── user.py
    |
    ├── notifications/
    │   └── notifier.py
    |
    ├── tests/
    │   └── ...
    |
    ├── transform/
    │   └── transform_data.py
    |
    ├── utils/
    │   └── logger.py
    |
    ├── dashboard_app.py
    ├── main.py
    ├── config.py
    ├── create_table.py
    ├── docker-compose.yml
    ├── .env.example
    ├── pytest.ini
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

Installation

1. Clone the Repository

    git clone https://github.com/shahanazpr/enterprise-etl-pipeline.git

2. Navigate to the Project Directory

    cd enterprise-etl-pipeline

3. Create a Virtual Environment

    python -m venv .venv

4. Activate the Virtual Environment

Windows:

    .venv\Scripts\activate

Linux/macOS:

    source .venv/bin/activate

5. Install Dependencies

    pip install -r requirements.txt

------------------------------------------------------------------------

Environment Configuration

Create a .env file in the project root.

For local Windows execution, PostgreSQL can be configured as:

    API_URL=https://jsonplaceholder.typicode.com/users

    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=airflow
    DB_USER=your_username
    DB_PASSWORD=your_password

    LOG_LEVEL=INFO

    EMAIL_SENDER=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    EMAIL_RECEIVER=receiver_email@gmail.com

    AWS_ACCESS_KEY_ID=your_access_key
    AWS_SECRET_ACCESS_KEY=your_secret_key
    AWS_REGION=ap-south-1
    S3_BUCKET_NAME=your_bucket_name

Never commit the real .env file, passwords, AWS credentials, email
credentials, or other secrets to GitHub.

The repository includes .env.example as a safe configuration template.

Docker Database Configuration

When the ETL application runs inside Docker Compose, the PostgreSQL
service hostname is:

    DB_HOST=postgres

When the Streamlit dashboard is run directly from Windows, use:

    DB_HOST=localhost

This assumes PostgreSQL port 5432 is exposed by Docker Compose.

------------------------------------------------------------------------

Database Setup

Create the required database tables:

    python create_table.py

The pipeline uses PostgreSQL with SQLAlchemy ORM for database
operations.

The loading stage performs an upsert:

-   Existing user IDs are updated.
-   New user IDs are inserted.

------------------------------------------------------------------------

Running the ETL Pipeline

Run the complete ETL pipeline:

    python main.py

The pipeline performs:

1.  Data extraction
2.  Record validation
3.  Raw JSON generation
4.  Optional S3 upload
5.  Data transformation
6.  PostgreSQL loading/upsert
7.  Logging
8.  Notification handling

------------------------------------------------------------------------

AWS S3 Raw Data Storage

AWS S3 integration is supported for storing raw extracted JSON data.

When S3 is configured, objects are organized by execution date:

    raw_data/YYYY-MM-DD/users.json

Example:

    raw_data/2026-08-24/users.json

S3 upload failures are automatically retried using Tenacity.

S3 is an optional cloud-storage component. If an S3 bucket is not
configured, the pipeline logs a warning and skips the upload while
continuing with the remaining ETL stages. This allows the project to run
locally without requiring AWS credentials.

------------------------------------------------------------------------

Apache Airflow

The ETL pipeline can be orchestrated using Apache Airflow.

The Airflow DAG automates the ETL workflow and provides a UI for:

-   Triggering pipeline runs
-   Monitoring task status
-   Viewing task logs
-   Inspecting execution history

The DAG is located at:

    dags/etl_pipeline.py

------------------------------------------------------------------------

Docker Support

The project includes Docker Compose support.

Start the services:

    docker compose up -d

Check the services:

    docker compose ps

Stop the services:

    docker compose down

Docker provides a consistent local environment for the database and
Airflow components.

------------------------------------------------------------------------

Streamlit Monitoring Dashboard

The project includes a Streamlit dashboard for monitoring ETL pipeline
activity.

Run the dashboard from the project root:

    streamlit run dashboard_app.py

Open:

    http://localhost:8501

Dashboard Features

The dashboard provides:

-   Pipeline run status
-   Total number of runs
-   Success rate
-   Average run duration
-   Last run status
-   Stage duration per run
-   Validation outcomes
-   Warning and error counts
-   Recent pipeline run history
-   Pipeline output/log information
-   PostgreSQL warehouse row count
-   Manual pipeline execution using the Run Pipeline Now button
-   Refresh functionality

The dashboard reads pipeline information from PostgreSQL and application
log data.

Dashboard Workflow

    Streamlit Dashboard
            |
            +--> PostgreSQL
            |      |
            |      +--> Warehouse records
            |
            +--> Pipeline Logs
            |      |
            |      +--> Run status / duration / warnings / errors
            |
            +--> Run Pipeline Now
                   |
                   v
                 main.py
                   |
                   v
              ETL Pipeline

------------------------------------------------------------------------

Testing

Run the automated test suite:

    python -m pytest

The repository includes pytest.ini so pytest does not attempt to collect
Airflow-generated log directories as tests.

The test suite covers the main ETL components and functionality.

------------------------------------------------------------------------

Logging

The pipeline uses structured logging to record:

-   Pipeline start and completion
-   Extraction status
-   Number of records extracted
-   Validation results
-   Transformation status
-   Database loading status
-   S3 upload status
-   Warnings
-   Errors
-   Stage execution duration

------------------------------------------------------------------------

Environment Variables

  Variable                Description
  ----------------------- -------------------------------------------
  API_URL                 REST API endpoint used to fetch user data
  DB_HOST                 PostgreSQL database host
  DB_PORT                 PostgreSQL database port
  DB_NAME                 PostgreSQL database name
  DB_USER                 PostgreSQL username
  DB_PASSWORD             PostgreSQL password
  LOG_LEVEL               Application logging level
  EMAIL_SENDER            Sender email address for notifications
  EMAIL_PASSWORD          Email password or app password
  EMAIL_RECEIVER          Recipient email address for alerts
  AWS_ACCESS_KEY_ID       AWS access key
  AWS_SECRET_ACCESS_KEY   AWS secret key
  AWS_REGION              AWS region
  S3_BUCKET_NAME          S3 bucket used for raw-data storage

------------------------------------------------------------------------

Current Status

Completed

-   Project setup
-   REST API extraction
-   Data validation
-   Data transformation
-   PostgreSQL database integration
-   SQLAlchemy ORM
-   Upsert-based database loading
-   Environment-based configuration
-   AWS S3 integration and optional upload handling
-   Date-based S3 organization
-   S3 retry handling
-   Structured logging
-   Email notification support
-   Unit testing
-   Pytest configuration
-   GitHub integration
-   Apache Airflow orchestration
-   Airflow pipeline execution
-   Docker support
-   Streamlit monitoring dashboard
-   Pipeline monitoring and run history
-   Project documentation

Future Improvements

-   Additional dashboard monitoring features
-   More extensive test coverage
-   Additional ETL data sources
-   Enhanced pipeline alerting
-   Further cloud deployment and monitoring

------------------------------------------------------------------------

Repository

GitHub: https://github.com/shahanazpr/enterprise-etl-pipeline

------------------------------------------------------------------------

Team Members

-   Shahanaz P
-   Yuvadarshini R
-   Kavitha KC
-   Manasa V
-   Varshitha

------------------------------------------------------------------------

Internship

Developed as part of the Zaalima Development Internship.