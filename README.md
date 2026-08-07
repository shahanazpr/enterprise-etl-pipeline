<<<<<<< HEAD
# Enterprise ETL Pipeline & Data Warehouse Synchronizer

## Overview

This project is a production-style ETL (Extract, Transform, Load) pipeline developed in Python.

The pipeline extracts user data from an external REST API, transforms it into a clean format, and loads it into a PostgreSQL database using SQLAlchemy for further analysis.

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
- Transform JSON data into CSV
- Load data into PostgreSQL
- SQLAlchemy ORM integration
- Pydantic configuration using `.env`
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

LOG_LEVEL=INFO
```

---

### Environment Variables

| Variable | Description |
|----------|-------------|
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

## Running Unit Tests

Run all tests using:

```bash
pytest
```

GitHub Actions automatically runs these tests whenever a Pull Request is created.

---


=======
>>>>>>> origin/main
## Current Status

### Completed

- Project Setup
- API Extraction
- Data Validation
- Data Transformation
- PostgreSQL Integration
- SQLAlchemy ORM
- Pydantic Configuration
- Retry Logic (Tenacity)
- Logging
<<<<<<< HEAD
- Email Notifications
- Unit Testing
- Apache Airflow
- GitHub Actions CI

### Upcoming

- Docker Support
- Additional ETL Enhancements

---

## Author

**Shahanaz P**

## Team Members

Shahanaz p

Yuvadarshini R

Kavitha

Manasa v

Varshitha



Developed as part of the Zaalima Development Internship.
=======
- Incremental Loading (UPSERT)
- Unit Testing
- GitHub Integration

### Upcoming

- Retry Logic
- Apache Airflow
- Docker
>>>>>>> origin/main
