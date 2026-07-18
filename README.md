# Enterprise ETL Pipeline & Data Warehouse Synchronizer

## Overview

This project is a production-style ETL (Extract, Transform, Load) pipeline developed in Python.

The pipeline extracts user data from an external REST API, transforms it into a clean format, and loads it into a PostgreSQL database using SQLAlchemy for further analysis.

This project is being developed as part of the Zaalima Development Internship.

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

```
enterprise-etl-pipeline/

├── data/
├── docs/
├── extract/
├── load/
├── models/
├── tests/
├── transform/
├── utils/
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

```bash
git clone https://github.com/shahanazpr/enterprise-etl-pipeline.git

cd enterprise-etl-pipeline

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

## Current Status

### Completed

- Project setup
- API Extraction
- Data Transformation
- PostgreSQL Database Integration
- SQLAlchemy ORM
- Pydantic Configuration
- Logging
- GitHub Integration

### Upcoming

- Retry Logic
- Apache Airflow
- Docker
- Unit Testing

---

## Author

**Shahanaz P**

## Team Members

shahanaz p

yuvadharshini R

kavitha

manasa v

varshitha



Developed as part of the Zaalima Development Internship.
