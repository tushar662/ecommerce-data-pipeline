# E-Commerce Data Engineering Pipeline

A modular end-to-end ETL pipeline built with Python, Pandas, PostgreSQL, Pytest, Git, GitHub, and Jenkins.

This project extracts e-commerce order data from the Olist Brazilian E-Commerce Public Dataset, transforms and validates the data, and loads the processed records into PostgreSQL.

Jenkins is used for Continuous Integration (CI) to automatically install dependencies, run automated tests, and execute the ETL pipeline.

---

## Project Overview

The main objective of this project is to build a practical Data Engineering pipeline that demonstrates the complete ETL lifecycle:

```text
E-Commerce CSV Data
        |
        v
    Extraction
        |
        v
   Transformation
        |
        v
     Validation
        |
        v
 PostgreSQL Loading
```

The project demonstrates:

- ETL pipeline design
- Data transformation using Pandas
- Data quality checks
- Data validation
- PostgreSQL database loading
- Idempotent data loading
- Logging
- Error handling
- Automated testing
- Environment-based configuration
- Secure credential handling
- Git/GitHub version control
- Jenkins Continuous Integration

---

# Architecture

```text
                         GitHub
                           |
                           v
                        Jenkins
                           |
                           v
                 Install Dependencies
                           |
                           v
                      Run Pytest
                           |
                     Tests Pass
                           |
                           v
                     Run ETL
                           |
                           v
                    Extract CSV
                           |
                           v
                    Transform Data
                           |
              +------------+------------+
              |            |            |
              v            v            v
        Date Transform  Orders      Delivery
                           |
                           v
                     Data Validation
                           |
                           v
                       PostgreSQL
                           |
                           v
                      orders table
```

---

# ETL Pipeline

```text
Extract
   |
   v
Transform Dates
   |
   v
Transform Orders
   |
   v
Transform Delivery
   |
   v
Validate
   |
   v
Load into PostgreSQL
```

The complete workflow is orchestrated by `main.py`.

---

# Dataset

This project uses the Brazilian E-Commerce Public Dataset by Olist.

The complete Olist dataset contains approximately 99,000 orders.

The main order dataset is:

```text
data/raw/olist_orders_dataset.csv
```

The original order dataset contains:

```text
order_id
customer_id
order_status
order_purchase_timestamp
order_approved_at
order_delivered_carrier_date
order_delivered_customer_date
order_estimated_delivery_date
```

For Jenkins CI and development, a smaller 1,000-row sample is used:

```text
data/sample/orders_sample.csv
```

This keeps CI execution fast while maintaining the same transformation and validation logic.

---

# Project Structure

```text
ecommerce-data-pipeline/
|
├── data/
│   |
│   ├── raw/
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_geolocation_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   └── product_category_name_translation.csv
│   │
│   └── sample/
│       └── orders_sample.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── transform_dates.py
│   ├── transform_orders.py
│   ├── transform_delivery.py
│   ├── validate.py
│   ├── load.py
│   └── logger.py
│
├── tests/
│   ├── test_transformations.py
│   └── test_validation.py
│
├── sql/
│   └── schema.sql
│
├── main.py
├── Jenkinsfile
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

---

# File Responsibilities

## main.py

`main.py` is the main pipeline orchestrator.

It calls all ETL stages in the correct order:

```text
Extract
    |
    v
Transform Dates
    |
    v
Transform Orders
    |
    v
Transform Delivery
    |
    v
Validate
    |
    v
Load
```

It also handles pipeline-level exceptions and records the execution status through the logger.

---

## src/extract.py

Responsible for extracting the order dataset.

The module supports two modes:

```text
Sample dataset
Full raw dataset
```

Sample dataset:

```text
data/sample/orders_sample.csv
```

Full dataset:

```text
data/raw/olist_orders_dataset.csv
```

The main function is:

```python
load_orders(use_sample=False)
```

The current pipeline uses:

```python
extract_orders(use_sample=True)
```

Therefore Jenkins currently processes the 1,000-row sample dataset.

---

## src/transform_dates.py

Responsible for date-related transformations.

The following columns are converted into Pandas datetime values:

```text
order_purchase_timestamp
order_approved_at
order_delivered_carrier_date
order_delivered_customer_date
order_estimated_delivery_date
```

Additional columns are created:

```text
purchase_date
purchase_year
purchase_month
purchase_day
purchase_weekday
```

---

## src/transform_orders.py

Performs order-level data quality checks.

The module reports:

- Duplicate order IDs
- Duplicate customer IDs
- Order status distribution
- Missing values

The duplicate customer check is informational because the same customer can have multiple orders.

---

## src/transform_delivery.py

Creates delivery-related metrics.

### delivery_days

Calculates the number of days between:

```text
order_purchase_timestamp
          |
          v
order_delivered_customer_date
```

### delivery_date_missing

Identifies delivered orders where the customer delivery date is missing.

### days_late

Calculates:

```text
Actual Delivery Date
        -
Estimated Delivery Date
```

### delivery_status

Classifies delivered orders as:

```text
On Time
Late
Unknown
```

---

## src/validate.py

Performs critical data validation before loading into PostgreSQL.

Current validation rules:

1. `order_id` cannot contain null values.
2. `order_id` cannot contain duplicate values.

If validation fails, a `ValueError` is raised and the pipeline stops before loading the data into PostgreSQL.

---

## src/load.py

Responsible for loading the transformed data into PostgreSQL.

The module uses Psycopg for the PostgreSQL connection.

Database configuration is imported from:

```text
src/config.py
```

The loader uses PostgreSQL conflict handling so repeated executions do not create duplicate orders.

---

## src/config.py

Contains environment-based database configuration.

The application reads:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
POSTGRES_PASSWORD
```

The non-sensitive database values have local defaults.

The PostgreSQL password is read from the environment and is not stored directly in the Python source code.

---

## src/logger.py

Provides the application logging system.

The logger records:

- Pipeline start
- Extraction start/completion
- Transformation start/completion
- Validation start/completion
- Database loading
- Pipeline completion
- Pipeline failures

Logs are written to:

```text
pipeline.log
```

The log file is excluded from Git using `.gitignore`.

---

## tests/

Contains automated tests for transformations and validation.

Current test files:

```text
tests/test_transformations.py
tests/test_validation.py
```

The current test suite contains 5 tests.

---

## sql/schema.sql

Contains the PostgreSQL database schema.

It creates the `orders` table and the required indexes.

---

## Jenkinsfile

Defines the Jenkins Continuous Integration pipeline.

The current stages are:

```text
Install Dependencies
        |
        v
Run Tests
        |
        v
Run Pipeline
```

---

## pytest.ini

Contains the Pytest configuration:

```ini
[pytest]
pythonpath = .
```

This allows tests to import modules from the `src` package.

---

# Technologies Used

## Programming

- Python

## Data Processing

- Pandas

## Database

- PostgreSQL
- Psycopg

## Testing

- Pytest

## CI

- Jenkins

## Version Control

- Git
- GitHub

---

# PostgreSQL

The current project uses PostgreSQL as the target database.

Local configuration:

```text
Host: localhost
Port: 5433
Database: ecommerce_db
User: postgres
Table: orders
```

The database schema is stored in:

```text
sql/schema.sql
```

---

# Database Schema

The `orders` table contains 17 columns:

```text
order_id
customer_id
order_status
order_purchase_timestamp
order_approved_at
order_delivered_carrier_date
order_delivered_customer_date
order_estimated_delivery_date
purchase_date
purchase_year
purchase_month
purchase_day
purchase_weekday
delivery_days
delivery_date_missing
days_late
delivery_status
```

---

# Primary Key

The primary key is:

```text
order_id
```

`order_id` is the unique identifier for an order.

It is used during:

```text
Data Validation
       |
       v
PostgreSQL Primary Key
       |
       v
ON CONFLICT handling
```

---

# Database Indexes

The database schema creates indexes on:

```text
order_status
purchase_date
```

The primary key also has its own index.

---

# Idempotent Loading

The database loader uses:

```sql
ON CONFLICT (order_id)
DO UPDATE
```

This allows the pipeline to be executed multiple times without creating duplicate order records.

Example:

```text
First Pipeline Run
       |
       v
1000 orders inserted

Second Pipeline Run
       |
       v
Existing order_id detected
       |
       v
Existing record updated
```

---

# Configuration

The project uses environment variables instead of hardcoding database credentials.

Required variables:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
POSTGRES_PASSWORD
```

Default local values:

```text
DB_HOST=localhost
DB_PORT=5433
DB_NAME=ecommerce_db
DB_USER=postgres
```

Only the PostgreSQL password needs to be supplied securely.

---

# Local Environment Configuration

On Windows PowerShell:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5433"
$env:DB_NAME="ecommerce_db"
$env:DB_USER="postgres"
$env:POSTGRES_PASSWORD="YOUR_POSTGRES_PASSWORD"
```

Do not commit the actual password to GitHub.

Never place credentials inside:

```text
Python files
Jenkinsfile
README.md
Git commits
```

---

# Local Setup

## 1. Clone the Repository

Using HTTPS:

```bash
git clone https://github.com/tushar662/ecommerce-data-pipeline.git
```

Or using SSH:

```bash
git clone git@github.com:tushar662/ecommerce-data-pipeline.git
```

Move into the project:

```bash
cd ecommerce-data-pipeline
```

---

## 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

The project dependencies are:

```text
pandas==3.0.5
psycopg[binary]
pytest
```

---

# PostgreSQL Setup

Create a PostgreSQL database:

```text
ecommerce_db
```

The project expects PostgreSQL to run on:

```text
localhost:5433
```

Open:

```text
sql/schema.sql
```

Execute the schema against `ecommerce_db`.

This creates the `orders` table and indexes.

---

# Configure the Database

Set the environment variables:

```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5433"
$env:DB_NAME="ecommerce_db"
$env:DB_USER="postgres"
$env:POSTGRES_PASSWORD="YOUR_POSTGRES_PASSWORD"
```

---

# Test PostgreSQL Connection

Run:

```powershell
python -c "from src.load import connect_database; conn=connect_database(); conn.close()"
```

Expected:

```text
PostgreSQL connection successful!
```

---

# Run Automated Tests

Run:

```powershell
python -m pytest
```

Expected result:

```text
5 passed
```

---

# Run the Complete ETL Pipeline

Run:

```powershell
python main.py
```

The pipeline executes:

```text
Extract
   |
   v
Transform Dates
   |
   v
Transform Orders
   |
   v
Transform Delivery
   |
   v
Validate
   |
   v
Load PostgreSQL
```

Expected final result:

```text
Pipeline completed successfully
Final rows: 1000
Final columns: 17
```

---

# Verify PostgreSQL Data

After the pipeline finishes:

```sql
SELECT COUNT(*)
FROM orders;
```

Expected:

```text
1000
```

View records:

```sql
SELECT *
FROM orders
LIMIT 10;
```

Check order statuses:

```sql
SELECT
    order_status,
    COUNT(*)
FROM orders
GROUP BY order_status
ORDER BY COUNT(*) DESC;
```

---

# Jenkins CI

Jenkins is used for Continuous Integration.

The Jenkins pipeline automatically performs:

```text
GitHub
   |
   v
Checkout
   |
   v
Install Dependencies
   |
   v
Run Pytest
   |
   v
Run ETL Pipeline
   |
   v
PostgreSQL
```

---

# Jenkins Pipeline Stages

## Stage 1 — Install Dependencies

Jenkins runs:

```powershell
python -m pip install -r requirements.txt
```

## Stage 2 — Run Tests

Jenkins runs:

```powershell
python -m pytest
```

All tests must pass before the ETL pipeline starts.

## Stage 3 — Run Pipeline

Jenkins executes:

```powershell
python main.py
```

The pipeline then performs the complete ETL process.

---

# Jenkins Credentials

The PostgreSQL credentials are stored securely in Jenkins.

Credential ID:

```text
postgres-db
```

Credential type:

```text
Username with password
```

The Jenkinsfile uses:

```groovy
withCredentials([
    usernamePassword(
        credentialsId: 'postgres-db',
        usernameVariable: 'DB_USER',
        passwordVariable: 'POSTGRES_PASSWORD'
    )
])
```

The password is masked in Jenkins console output.

The password is not stored in GitHub.

---

# Jenkins Execution Flow

```text
GitHub Repository
        |
        v
Jenkins Checkout
        |
        v
Install Dependencies
        |
        v
Run Pytest
        |
        v
5 Tests Passed
        |
        v
Run main.py
        |
        v
Extract 1000 Rows
        |
        v
Transform Data
        |
        v
Validate Data
        |
        v
Connect PostgreSQL
        |
        v
Load 1000 Rows
        |
        v
Build SUCCESS
```

If tests fail:

```text
Run Tests
    |
    v
FAIL
    |
    v
Jenkins stops
    |
    v
ETL does not run
```

---

# Final Verified Result

The complete pipeline has been tested locally and through Jenkins.

Current verified result:

```text
Input Rows:          1000
Input Columns:       8
Output Rows:         1000
Output Columns:      17
Automated Tests:     5 passed
PostgreSQL Load:     Successful
Jenkins Build:       SUCCESS
```

---

# Data Quality Checks

The pipeline currently checks:

```text
Duplicate order IDs
Duplicate customer IDs
Missing values
Missing delivery dates
Null order IDs
Duplicate order IDs during validation
```

Critical validation is performed before PostgreSQL loading.

---

# Error Handling

The main pipeline uses exception handling.

If a pipeline stage fails:

```text
Pipeline Error
      |
      v
Logger records error
      |
      v
Exception is raised
      |
      v
Pipeline stops
      |
      v
Jenkins build fails
```

This prevents silent pipeline failures.

---

# Logging

Pipeline logs are stored in:

```text
pipeline.log
```

Example events logged:

```text
Ecommerce Data Pipeline Started
Starting extraction
Extraction completed
Starting date transformation
Date transformation completed
Starting order transformation
Order transformation completed
Starting delivery transformation
Delivery transformation completed
Starting data validation
Data validation completed
Starting database load
Database load completed
Pipeline completed successfully
```

The log file is ignored by Git.

---

# Sample Dataset vs Full Dataset

The project supports both sample and full datasets.

## Sample Dataset

```text
data/sample/orders_sample.csv
```

Used for:

- Jenkins CI
- Fast testing
- Development

Current size:

```text
1000 rows
```

## Full Dataset

```text
data/raw/olist_orders_dataset.csv
```

Used for processing the complete order dataset locally.

The raw data is intentionally excluded from Git.

---

# Processing the Full Dataset

The current `main.py` uses:

```python
extract_orders(use_sample=True)
```

This selects:

```text
data/sample/orders_sample.csv
```

To process the full raw dataset locally, change it to:

```python
extract_orders(use_sample=False)
```

The extraction module will then use:

```text
data/raw/olist_orders_dataset.csv
```

The full dataset must exist locally.

---

# Git and GitHub Workflow

Check repository status:

```powershell
git status
```

View changes:

```powershell
git diff
```

View recent commits:

```powershell
git log --oneline -5
```

Check remote repository:

```powershell
git remote -v
```

Add changes:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Describe your change"
```

Push:

```powershell
git push
```

Pull latest changes:

```powershell
git pull
```

---

# Recommended Development Workflow

```text
Change Code
    |
    v
Run Tests
    |
    v
Run Pipeline Locally
    |
    v
Verify PostgreSQL
    |
    v
git status
    |
    v
git diff
    |
    v
git add
    |
    v
git commit
    |
    v
git push
    |
    v
Jenkins CI
```

Example:

```powershell
python -m pytest
python main.py

git status
git diff

git add .
git commit -m "Update transformation logic"
git push
```

---

# .gitignore

The project ignores:

```text
data/raw/
__pycache__/
*.pyc
.venv/
venv/
pipeline.log
```

This prevents large raw datasets, Python cache, virtual environments, and local logs from being committed.

---

# Security

Database credentials are not stored in source code.

Local development uses:

```text
POSTGRES_PASSWORD
```

Jenkins uses:

```text
Jenkins Credentials
```

Never commit:

```text
Passwords
API keys
Tokens
Private credentials
```

to GitHub.

If a credential is accidentally exposed, rotate it immediately and remove the exposed secret from repository history.

---

# Current Scope

The current implementation focuses on the Olist order ETL pipeline.

The repository contains other Olist datasets, but the current PostgreSQL pipeline processes:

```text
olist_orders_dataset.csv
```

The current project does not implement:

```text
Docker
Kubernetes
Airflow
Kafka
Spark
Cloud Deployment
```

These technologies are intentionally outside the scope of this implementation.

---

# Possible Future Improvements

The pipeline can later be extended with:

- Customer dimension
- Product dimension
- Seller dimension
- Order items
- Payment data
- Review data
- Analytical SQL queries
- Data quality reports
- Pipeline scheduling
- Cloud deployment
- Data warehouse modeling

These are future improvements and are not required for the current pipeline.

---

# Final Project Status

The following components have been implemented and tested:

```text
ETL Pipeline              ✅
Data Extraction           ✅
Data Transformation       ✅
Data Validation           ✅
PostgreSQL                ✅
Idempotent Loading        ✅
Logging                   ✅
Error Handling            ✅
Automated Tests           ✅
Configuration             ✅
Environment Variables     ✅
Secure Credentials        ✅
Git                       ✅
GitHub                    ✅
Jenkins CI                ✅
End-to-End Testing        ✅
Documentation             ✅
```

Final verified Jenkins result:

```text
5 tests passed
1000 rows processed
17 final columns
PostgreSQL load successful
Jenkins build successful
```

