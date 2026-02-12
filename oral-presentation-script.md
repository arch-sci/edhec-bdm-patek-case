# Presentation Script


### Context & Data Strategy
"We started with a single, unrefined dataset in BigQuery: `raw_data`.
**The Problem:** It was a mess of mixed currencies (USD, GBP, CHF), making direct comparison impossible.
**The Engineering Fix:** We didn't just clean the data; we built an **Exchange Rate Scraper** (`fx_rates.py`). This module fetches historical rates from an API and normalizes every single watch price to EUR directly in the pipeline."




***

### The Concept: "The Portable Data Factory"

Imagine you built a **Data Factory** inside a shipping container.
*   **Your Mac** is the dock. It’s messy.
*   **Docker** is the shipping container. Inside, it is pristine. It has Python, the exact libraries you need, and your code.
*   **BigQuery** is the external warehouse. It is now organized into two zones: **Raw Storage** (`patek_raw` for backup/dirty data) and **Production** (`patek` for clean data).
*   **GitHub** is the blueprint storage. If your computer explodes, the factory instructions are safe there.

You have created a system where **one command** spins up the factory, does the work, and shuts down.

---

### The 3 Scenarios

#### Scenario A: The "One-Click Update" (Production Run) <span style="color:darkgreen;">(--- show dockerfile >> makefile)</span>
**Situation:** You want to refresh all data from the raw source, fetch today's exchange rates, and retrain your pricing model.

**1. You do this:**
*   **Where:** Terminal (inside your project folder).
*   **Command:**
    ```bash
    docker compose up --build
    ```

**2. What happens inside the machine:**
*   **Build:** Docker reads `Dockerfile`. It downloads Python, installs `pandas`, `sklearn`, etc.
*   **Start:** The container wakes up. It looks at the last line of `Dockerfile`: `CMD ["make", "pipeline"]`.
*   **Execution (The `Makefile` takes over):**
    1.  **Step 1 (`data.py`):** Connects to the **Raw BigQuery Table (`patek_raw`)**. Downloads the full history (including dirty rows). **Filters/Cleans** it in Python (removing null prices). Saves `patek_philippe_data.csv`.
    2.  **Step 2 (`fx_rates.py`):**
        *   Fetches exchange rates for valid watches.
        *   Uploads rates to BigQuery.
        *   **CRITICAL STEP:** It runs a **SQL UPDATE** directly inside BigQuery. It joins your price table with the rate table to generate the `price_EUR` column server-side. **Zero data movement. Millisecond execution.**
        *   Saves `fx_rates.csv` locally for PowerBI.
    3.  **Step 3 (`model.py`):** Loads the local CSVs. Trains a Random Forest AI to predict prices. Saves predictions to `model_predictions.csv`.
*   **Finish:** The container stops.

**3. The Result:**
*   Three new CSV files appear magically in your project folder on your Mac, and BigQuery is fully enriched with EUR prices.

---

#### Scenario B: The "Visual Analysis" (The Notebook) <span style="color:darkgreen;">(--- show makefile)</span>
**Situation:** You want to manually explore the data, draw charts, or debug code using Jupyter Notebooks.

**1. You do this:**
*   **Where:** Terminal.
*   **Command:**
    ```bash
    docker compose run --service-ports app make notebook
    ```
    *(Translation: "Docker, run the 'app' container, open the network ports, and instead of the default command, run the 'notebook' command defined in my Makefile.")*

**2. What happens:**
*   The container starts but **stays alive**.
*   It launches a Jupyter Server inside the container.
*   It prints a URL in your terminal starting with `http://127.0.0.1:8888...`.

**3. You do this next:**
*   **Where:** Chrome / Safari.
*   **Action:** Copy-paste that URL or Cmd+Click it.
*   **Action:** Open `test-fx_visualization.ipynb`.
*   **Action:** Click "Run All".

**4. What happens inside:**
*   Python runs **inside** the container. It executes the code to query BigQuery directly (using your new table structure) and plot the FX history.

---

#### Scenario C: PowerBI Update (The Dashboard)
**Situation:** At first, we could not connect PowerBI to BigQuery (license/tech restrictions), so we used the "Relational CSV" method.

**1. Do this:**
*   Perform **Scenario A** first (run `docker compose up --build`).
*   Wait for the "✅ Success" messages in the terminal.

**2. Do this next:** <span style="color:darkgreen;">(--- show dashboard folder)</span>
*   **Where:** PowerBI (Desktop app on your computer).
*   **Action:** Open the `.pbix` file.
*   **Action:** Click the **Refresh** button.

**3. What happens:**
*   PowerBI looks at the `patek_philippe_data.csv` and `fx_rates.csv` created by the running of the container your hard drive.
*   It notices they have changed (Scenario A updated them).
*   It ingests the new rows.
*   It uses the relationship you built (linking `currency` to `base_currency`) to update your charts.



***

#### Scenario D: The Real-Time Upgrade (Looker Studio)
**Situation:** We wanted a cloud-native solution for Data Vis.

**1. The Architecture Shift:**
*   We connected **Looker Studio** directly to the `patek` production table in BigQuery.

**2. The Result:**
*   **No CSVs:** The dashboard reads directly from the warehouse.
*   **No "Refresh" Button:** As soon as the Docker container finishes its `UPDATE` command in BigQuery, the dashboard reflects the changes instantly.
*   This is a fully automated, end-to-end cloud pipeline.



---

### Summary of Files & Roles

| File | Role |
| :--- | :--- |
| **Dockerfile** | The Blueprint. Tells Docker "Install Python, then run `make pipeline`". |
| **docker-compose.yml** | The Manager. Handles credentials (keys) and volumes (saving files to Mac). |
| **Makefile** | The Shortcut Menu. Defines what "pipeline", "notebook", and "clean" actually do. |
| **data.py** | **Extractor.** BigQuery (`patek_raw`) -> Python Cleaning -> CSV. |
| **fx_rates.py** | **Enricher.** API -> BigQuery. **Perform SQL Update (Calculate `price_EUR`)**. |
| **model.py** | **Predictor.** CSV -> Machine Learning -> CSV. |
| **migrate.py** | **Admin Tool.** One-time script used to create `patek_raw` (backup) and scrub the production `patek` table. |