# Enterprise ETL Pipeline & Data Warehouse Synchronizer

## Overview

This project is a production-style ETL (Extract, Transform, Load) pipeline developed in Python.

The pipeline extracts user data from an external REST API, validates and transforms it, stores raw JSON data in AWS S3, and loads the processed data into a PostgreSQL database using SQLAlchemy.

This project is being developed as part of the Zaalima Development Internship.

## Project Architecture

```text
              REST API
                  │
                  ▼
          Extract (Requests)
                  │
                  ▼
       Validate (Pydantic)
                  │
                  ▼
      Transform (Pandas)
                  │
                  ▼
 Load (SQLAlchemy + PostgreSQL)
                  │
                  ▼
 Logging & Email Notifications
                  │
                  ▼
         Apache Airflow
```

---

## Features

- Extract data from REST APIs
- Validate extracted data using Pydantic
- Store raw JSON data in AWS S3
- Organize S3 files by date
- Retry failed S3 uploads
- Transform JSON data into CSV
- Load data into PostgreSQL
- SQLAlchemy ORM integration
- Environment-based configuration
- Logging support
- Modular project structure
- Git version control

---

## Tech Stack

- Python 3.14
- Requests
- Pandas
- PostgreSQL
- SQLAlchemy
- Pydantic Settings
- AWS S3
- Boto3
- Tenacity
- Logging

---

## Project Structure

```text
enterprise-etl-pipeline/
│
├── data/
│   ├── users.json
│   └── users.csv
│
├── dags/
│   └── etl_pipeline.py
│
├── extract/
│   └── extract_api.py
│
├── transform/
│   └── transform_data.py
│
├── load/
│   └── load_data.py
│
├── validation/
│   └── user_model.py
│
├── notifications/
│   └── notifier.py
│
├── models/
│   └── user.py
│
├── tests/
│
├── utils/
│   └── logger.py
│
├── .env.example
├── config.py
├── database.py
├── create_table.py
├── main.py
├── README.md
└── requirements.txt
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shahanazpr/enterprise-etl-pipeline.git
```

### 2. Navigate to the Project Directory

```bash
cd enterprise-etl-pipeline
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 5. Install the Required Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file with the following values:

```env
API_URL=https://jsonplaceholder.typicode.com/users

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=enterprise_etl

AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your_bucket_name

LOG_LEVEL=INFO
```

> Never commit real AWS credentials or other secrets to GitHub.

---

## AWS S3 Raw Data Storage

The pipeline uploads extracted raw JSON data to the configured AWS S3 bucket.

S3 objects are organized by date using the following structure:

```text
raw_data/YYYY-MM-DD/users.json
```

For example:

```text
raw_data/2026-08-10/users.json
```

Failed S3 uploads are automatically retried before the error is reported.

### Environment Variables

| Variable | Description |
|---|---|
| API_URL | REST API endpoint used to fetch user data |
| DB_HOST | PostgreSQL database host |
| DB_PORT | PostgreSQL database port |
| DB_NAME | PostgreSQL database name |
| DB_USER | PostgreSQL username |
| DB_PASSWORD | PostgreSQL password |
| LOG_LEVEL | Logging level |
| EMAIL_SENDER | Sender email address for notifications |
| EMAIL_PASSWORD | Sender email password/app password |
| EMAIL_RECEIVER | Recipient email address for alerts |

---

## How to Run

Create the database tables:

```bash
python create_table.py
```

Run the ETL pipeline:

```bash
python main.py
```

---

## Testing

Run the test suite using:

```bash
python -m pytest
```

The current test suite has been verified with:

```text
8 passed, 1 skipped
```

GitHub Actions automatically runs these tests whenever a Pull Request is created.

---

## Current Status

### Completed

- Project setup
- API Extraction
- Data Validation
- Data Transformation
- PostgreSQL Database Integration
- SQLAlchemy ORM
- Pydantic Configuration
- AWS S3 Raw Data Storage
- Date-based S3 organization
- S3 upload retry handling
- Logging
- Email Notifications
- Unit Testing
- GitHub Integration

### Upcoming

- Apache Airflow
- Docker Support
- Further pipeline monitoring improvements
- Additional ETL enhancements

---

## Author

**Shahanaz P**

## Team Members

- Shahanaz P
- Yuvadarshini R
- Kavitha KC
- Manasa V
- Varshitha

---

# Developed as part of the Zaalima Development Internship.
