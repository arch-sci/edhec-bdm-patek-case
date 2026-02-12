# Patek Philippe Data Engineering Pipeline

A fully containerized data pipeline that ingests Patek Philippe watch data, enriches prices with historical exchange rates, and optionally trains a Machine Learning model to predict values. Everything is designed for reproducibility, clarity, and cloud-native integration.

## 🏗 Architecture
- **BigQuery Storage Layers:**
  - `patek_raw`: Raw ingestion layer (backup/dirty data)
  - `patek`: Production table (cleaned & enriched)
  - `fx_rates`: Historical exchange rates

- **Pipeline (Dockerized "Portable Data Factory"):**
  1. **Extraction & Cleaning** — `data.py` pulls raw BigQuery data, sanitizes it, saves CSV snapshot.
  2. **FX Enrichment** — `fx_rates.py` fetches historical exchange rates, writes enriched table to BigQuery, updates `price_EUR` in-place, saves CSV locally.
  3. **Modeling (optional)** — `model.py` trains a Random Forest to predict prices, outputs `model_predictions.csv`.
  4. **Visualization** — Jupyter notebooks for interactive analysis; Looker Studio for real-time dashboards.

## 🚀 How to Use

### Scenario A — Production Run
Refresh all data, update FX rates, optionally retrain the model:
```bash
docker compose run --rm --service-ports app bash
# Inside container:
python -m patek_analysis.data
python -m patek_analysis.fx_rates
python -m patek_analysis.model  # optional
exit
````

* CSVs saved locally: `patek_philippe_data.csv`, `fx_rates.csv`, `model_predictions.csv`.
* BigQuery is updated; container removed automatically.

### Scenario B — Visual Analysis (Notebook)

Explore data or debug interactively:

```bash
docker compose run --rm --service-ports app make notebook
```

* Opens Jupyter; run notebooks like `fx_visualization.ipynb`.
* Exit server with Ctrl+C; container removed automatically.

### Scenario C — Dashboard (Looker Studio)

Cloud-native dashboards read directly from BigQuery:

* Setup: Connect Looker Studio to `patek` table.
* Trigger updates: Run Scenario A; dashboards refresh automatically.
* No local files or refresh buttons required.

## 🛠 Tech Stack

* Python 3.12
* Docker & Docker Compose
* Google BigQuery
* Pandas, Scikit-Learn, Google Cloud SDK

## 📂 Key Files

* `Dockerfile`, `docker-compose.yml`, `Makefile`, `requirements.txt`
* `patek_analysis/` → `data.py`, `fx_rates.py`, `model.py`
* `fx_visualization.ipynb`, `dashboard/`
* `secrets/` → Google service account key

**Principles:**

* Manual or Make commands control execution.
* Docker ensures reproducibility.
* CI/CD automates FX enrichment; ML is optional and downstream.
* Users see all outputs; no automatic BigQuery modifications outside the container.
