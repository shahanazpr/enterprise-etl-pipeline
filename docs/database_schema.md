# Enterprise ETL Pipeline Database Schema

## Overview

The Enterprise ETL Pipeline stores processed data in a PostgreSQL database. SQLAlchemy is used as the Object Relational Mapper (ORM) to define tables and interact with the database.

---

# Database

**Database Name:** enterprise_etl

**Database System:** PostgreSQL

**ORM:** SQLAlchemy

---

# Main Table: records

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| id | Integer | Primary Key |
| name | String | Name of the record |
| email | String | Email address |
| department | String | Department name |
| salary | Float | Employee salary |
| created_at | Timestamp | Record creation time |
| updated_at | Timestamp | Last update time |

---

# Entity Relationship

```
+-------------------------+
|        records          |
+-------------------------+
| id (PK)                 |
| name                    |
| email                   |
| department              |
| salary                  |
| created_at              |
| updated_at              |
+-------------------------+
```

---

# Database Operations

The ETL pipeline performs the following operations:

- Insert new records
- Update existing records
- Validate incoming data
- Handle transaction rollback on failure
- Maintain data integrity

---

# SQLAlchemy Model

The SQLAlchemy model represents the **records** table and provides object-oriented database interaction.

Example fields include:

- id
- name
- email
- department
- salary

---

# Future Improvements

- Add indexing for faster queries
- Support multiple tables
- Introduce foreign key relationships
- Add audit logging
- Partition large datasets

---

# Summary

The PostgreSQL database acts as the final destination of the ETL pipeline, ensuring structured, reliable, and scalable storage of transformed data.
