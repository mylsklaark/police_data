![Pipeline](https://github.com/mylsklaark/police_data/actions/workflows/pipeline.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)

# Overview

This project showcases a lightweight data pipeline by querying the UK Police API,
transforming the returned JSON data, and loading it as converted CSV files into a 
database that can be queried.

## Prerequisites

- Python 3.12
- pip

## Setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Data source

- Data comes from the UK Police open data API (data.police.uk)
- The pipeline queries the last_updated endpoint before ingesting to ensure it only requests published data
- Street level crimes is the specific endpoint used
- No authentication required
- Default location is Oxford, but can be configured

## Usage

The pipeline runs the following steps on the first of each month via GitHub actions. Manual runs are the exception, not the rule. Each run ingests the last 12 months of street-level crime data and commits the results back to the repository.

```bash
python src/ingest.py
python src/transform.py
python src/load.py
```

## Project structure

src/ingest.py       Fetches crime data from the API and saves raw JSON
src/transform.py    Transforms raw JSON into flattened CSVs
src/load.py         Loads processed CSVs into SQLite
tests/              Unit tests mirroring the src/ structure

## Data

Raw JSON responses are saved to data/raw/
Processed CSVs are saved to data/processed/
The SQLite database is at data/crime_data.db

## Schema

| Field | Description |
|-------|-------------|
| id | Crime ID from the API |
| category | Crime category |
| month | Month the crime was recorded (YYYY-MM) |
| latitude | Latitude of the crime location |
| longitude | Longitude of the crime location |
| street | Approximate street name |
| outcome_status | Latest recorded outcome category |