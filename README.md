# Enterprise ETL Pipeline & Data Warehouse Synchronizer

## Overview

This project is a production-style ETL (Extract, Transform, Load) pipeline developed in Python.

The pipeline extracts user data from an external REST API, transforms it into a clean format, and loads it into a database for further analysis.

This project is being developed as part of the Zaalima Development Internship.

---

## Features

- Extract data from REST APIs
- Transform JSON data into CSV
- Load data into SQLite database
- Logging support
- Environment variable configuration using `.env`
- Modular project structure
- Git version control

---

## Tech Stack

- Python 3.14
- Requests
- Pandas
- SQLite
- Python-dotenv
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
├── .env
├── .gitignore
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

## How to Run

1. Clone the repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the `.env` file.
4. Run the ETL pipeline.

## Run

```bash
python main.py
```

---

## Current Status

Completed

- Project setup
- API Extraction
- Data Transformation
- Database Loading
- Logging
- GitHub Integration

Upcoming

- Pydantic Validation
- SQLAlchemy
- PostgreSQL
- Retry Logic
- Apache Airflow
- Docker
- Unit Testing

---

## Author

Shahanaz p

Developed as part of the Zaalima Development Internship.