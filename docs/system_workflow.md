# Enterprise ETL Pipeline Workflow

## Overview

The Enterprise ETL Pipeline follows the Extract, Transform, and Load (ETL) process to move data from source files into a PostgreSQL database.

---

## Workflow

```
        CSV File
            │
            ▼
     Extract Module
            │
            ▼
   Data Validation & Cleaning
            │
            ▼
   Data Transformation
            │
            ▼
   Retry Logic (Tenacity)
            │
            ▼
     SQLAlchemy Models
            │
            ▼
   PostgreSQL Database
            │
            ▼
      Logging & Reports
```

---

## Module Description

### 1. Extract

- Reads CSV files.
- Checks whether the file exists.
- Loads data using Pandas.

---

### 2. Transform

- Removes duplicate records.
- Handles missing values.
- Converts data types.
- Standardizes column names.
- Validates records.

---

### 3. Load

- Connects to PostgreSQL.
- Inserts cleaned records.
- Updates existing records if required.
- Handles database errors.

---

### 4. Retry Mechanism

The project uses the **Tenacity** library to automatically retry failed database operations caused by temporary issues.

---

### 5. Logging

The pipeline records:

- Pipeline start
- Successful extraction
- Transformation status
- Database insertion
- Errors
- Completion status

---

## Future Enhancements

- Apache Airflow scheduling
- Email notifications
- Docker deployment
- Cloud database support
- Data quality reports

---

## Workflow Summary

Extract → Transform → Validate → Retry if Needed → Load → Log Results
