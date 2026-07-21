# Apache Airflow DAG Automation

## Overview

This project uses Apache Airflow to automate the ETL workflow.

The DAG executes the following tasks in sequence:

1. Extract data from API
2. Transform data
3. Load data into the database

## Schedule

Daily

## Task Flow

Extract Data
      ↓
Transform Data
      ↓
Load Data

## Retry Policy

- Retries: 2
- Retry Delay: 5 minutes

## Note

Apache Airflow is intended to run on Linux, Docker, or WSL2 environments. Native Windows execution is not officially supported.