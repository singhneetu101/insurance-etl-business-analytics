# Automated Insurance Portfolio ETL & Business Analytics Pipeline

## Project Overview

This project demonstrates an end-to-end ETL and Business Intelligence solution for an insurance company.

Regional offices submit insurance portfolio data in different Excel and CSV formats. The data contains inconsistent schemas, duplicate records, missing values, and invalid data.

The project automates the complete ETL process using Python, loads the curated dataset into Microsoft SQL Server, and visualizes business insights through Power BI.

---

# Business Problem

Insurance organizations receive portfolio data from multiple regional branches.

Challenges include:

- Multiple file formats (CSV & Excel)
- Different column names
- Duplicate policy records
- Missing premium values
- Missing customer information
- Invalid premium values
- Inconsistent product names
- Manual reporting effort

These issues delay reporting and reduce data quality.

---

# Solution

An automated ETL pipeline was developed to:

- Extract multiple source files
- Standardize schemas
- Clean and validate data
- Remove duplicates
- Generate business-ready datasets
- Load data into SQL Server
- Create interactive Power BI dashboards

---

# Technology Stack

- Python
- Pandas
- NumPy
- SQL Server
- SSMS
- Power BI
- Excel

---

# Project Architecture

Raw Insurance Files

↓

Python ETL Pipeline

↓

Data Validation & Cleaning

↓

SQL Server

↓

Business Analysis (SQL)

↓

Power BI Dashboard

---

# ETL Workflow

## Extract

- Read CSV files
- Read Excel files
- Merge multiple regional datasets

## Transform

- Standardize column names
- Handle missing values
- Remove duplicate policies
- Correct negative premium values
- Standardize product names
- Create derived business columns

## Load

- Export processed dataset
- Load into SQL Server
- Connect Power BI

---

# Dashboard KPIs

- Total Policies
- Total Premium
- Average Premium
- Active Policies
- Expired Policies
- Premium by Product
- Premium by Branch
- Policy Status
- Premium Band
- Data Quality Summary

---

# Repository Structure

```text
scripts/
sql/
dashboard/
images/
data/
```

---

# Future Enhancements

- Incremental ETL
- Automated SQL Loading
- Logging
- Data Quality Report
- Airflow Scheduling
- Azure Deployment

---

# Author

Neetu Singh
