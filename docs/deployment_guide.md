# Enterprise ETL Pipeline Deployment Guide

## Overview

This guide explains how to set up and run the Enterprise ETL Pipeline on a local machine.

---

# Prerequisites

Ensure the following software is installed:

- Python 3.10 or later
- PostgreSQL
- Git
- pip (Python Package Manager)

---

# Clone the Repository

```bash
git clone https://github.com/your-username/enterprise-etl-pipeline.git
cd enterprise-etl-pipeline
```

---

# Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment Variables

Create a `.env` file in the project root.

Example:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=enterprise_etl
DB_USER=postgres
DB_PASSWORD=your_password
```

---

# Run Database Migrations

If migrations are used:

```bash
alembic upgrade head
```

Otherwise, create the required tables before running the project.

---

# Run the ETL Pipeline

```bash
python main.py
```

---

# Run Unit Tests

```bash
pytest
```

---

# Verify Successful Execution

A successful run should:

- Read data from the source file.
- Transform and validate the data.
- Insert records into PostgreSQL.
- Display success logs without errors.

---

# Troubleshooting

## Database Connection Failed

- Verify PostgreSQL is running.
- Check database credentials.
- Confirm the database exists.

## Missing Dependencies

Run:

```bash
pip install -r requirements.txt
```

## Module Import Errors

Ensure the virtual environment is activated before running the project.

---

# Future Deployment

The project can be extended to support:

- Docker containers
- Apache Airflow scheduling
- CI/CD using GitHub Actions
- Cloud deployment (AWS, Azure, GCP)
