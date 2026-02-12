# Patek Philippe Data Engineering Pipeline

A **containerized, reproducible pipeline** that ingests luxury watch data, enriches it with historical exchange rates, and predicts prices using Machine Learning.

## 🏗 Architecture

This project follows a **lakehouse approach** with **Google BigQuery** as the single source of truth.

- **Storage Layers**
  - `patek_raw` → Raw ingestion backup
  - `patek` → Cleaned & enriched production data
  - `fx_rates` → Historical currency exchange rates

- **Pipeline Steps (Dockerized)**
  1. **Extraction & Cleaning:** `data.py` pulls raw data from BigQuery and sanitizes it.
  2. **Enrichment:** `fx_rates.py` fetches historical FX rates via API and updates `price_EUR` in BigQuery.
  3. **Transformation (SQL):** CTAS strategy merges data efficiently server-side.
  4. **Modeling:** `model.py` trains a Random Forest to predict watch prices.

## 🚀 Running the Pipeline

### Full Pipeline (Scenario A)
```bash
docker compose run --rm --service-ports app bash
```
Inside the container, execute the pipeline stepwise via python -m patek_analysis.<module> or follow the Presentation Script for guided steps.  

### Visual Exploration (Scenario B)
```bash
docker compose run --rm --service-ports app make notebook
```
Then open localhost:8888 in your browser to run Jupyter notebooks.

### Dashboard Updates (Scenario C)
Looker Studio reads directly from the patek table in BigQuery. Run Scenario A to refresh data; dashboards update automatically—no CSVs required.

## 🛠 Tech Stack
Language: Python 3.12
Container: Docker & Docker Compose
Cloud: Google BigQuery

Libraries: Pandas, Scikit-Learn, Google Cloud SDK

## 📂 Folder Overview

patek_analysis/ → Core Python modules (data.py, fx_rates.py, model.py)
fx_visualization.ipynb → Notebook for exploratory analysis
dashboard/ → Looker Studio or PowerBI .pbix files
Makefile → Shortcuts for pipeline steps
Dockerfile & docker-compose.yml → Container definitions
secrets/ → Place Google service account keys here

Tip: Always use --rm to prevent orphaned containers. ML runs are optional and safe; no production tables are overwritten automatically.