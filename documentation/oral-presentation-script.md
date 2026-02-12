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

#### Scenario A: Production Run <span style="color:darkgreen;">(look at the Dockerfile & Makefile)</span>

**Situation:** You want to refresh all data from the raw source, fetch today’s exchange rates, and optionally retrain your pricing model.

**1. You do this:**  
* **Step 0 — Start container interactively:**  
In your Terminal (inside your project folder), run  
    ```bash
    docker compose run --rm --service-ports app bash
    ```

**2. What you can run the container shell (stepwise demo):**  
* **Step 1 — Data extraction:**  
    ```bash
    python -m patek_analysis.data
    ```  
    - Connects to **Raw BigQuery table (`patek_raw`)**.  
    - Downloads full history (including dirty rows).  
    - Cleans data (removes null prices).  
    - Saves `patek_philippe_data.csv` locally.  

* **Step 2 — FX enrichment:**  
    ```bash
    python -m patek_analysis.fx_rates
    ```  
    - Fetches historical exchange rates for all valid watches.  
    - Writes enriched FX table to BigQuery.  
    - Updates `price_EUR` server-side in BigQuery (no data movement).  
    - Saves `fx_rates.csv` locally for analysis/PowerBI.  

* **Step 3 — ML / Model:**  
    ```bash
    python -m patek_analysis.model
    ```  
    - Re-does the data extraction to get the Patek data and clean it.  
    - Trains a Random Forest to predict prices.  
    - Prints R² score to terminal.  
    - Saves predictions to `model_predictions.csv`.  

* **Step 4 — Exit the Container shell :**  
    ```bash
    exit
    ```  


**3. The Result:**  
* CSV snapshots appear locally:  
    - `patek_philippe_data.csv`  
    - `fx_rates.csv`  
    - `model_predictions.csv` (if ML step run)  
* BigQuery is updated with EUR prices.  
* You control each step and see outputs; nothing runs automatically without your confirmation.  
* Container is removed automatically after exit (--rm).


---

#### Scenario B: The Visual Analysis (Notebooks) <span style="color:darkgreen;">(look at the makefile)</span>
**Situation:** You want to manually explore the data, draw charts, or debug code using Jupyter Notebooks. Or just quick notebook access to explore data without running everything in advance.

**1. You do this:**
*   **Where:** Terminal.
*   **Command:**
    ```bash
    docker compose run --rm --service-ports app make notebook
    ```
    *(Translation: "Docker, run the 'app' container, open the network ports, and instead of the default command, run the 'notebook' command defined in my Makefile. Also, --rm ensures the temporary container is deleted afterwards to avoid orphans.")*

**2. What happens:**
*   The container starts and **stays alive**.
*   It launches a Jupyter Server inside the container.
*   It prints a URL in your terminal starting with `http://127.0.0.1:8888...`. 
    Then, it "waits" for you do interact with the server and logs your interactions.

**3. You do this next:**
*   **Where:** Chrome / Safari.
*   **Action:** Copy-paste that URL or Cmd+Click it.
*   **Action:** For example, `test-fx_visualization.ipynb`.
*   **Action:** Click "Run All".

**4. What happens inside:**
*   Python runs **inside** the container. It executes the code to query BigQuery directly (using your new table structure) and plot the FX history.

**5. Exiting the Jupyter Server:**
* Close the tabs you opened.
* Ctrl+C once in the terminal to stop the server & confirm.
* Container is removed automatically (--rm)

---

#### Scenario C: The Dashboard (Looker Studio)

At first, we could not connect PowerBI to BigQuery (license/tech restrictions), so we used CSV snapshots in a fixed `.pbix` file (you can find it inside the `dashboard` folder).  
Now, we move to a fully connected, cloud-native solution for data visualization.

**Situation:** You want to access a Data Vis tool that reads directly from BigQuery and updates in real time.

**1. Architecture / Setup:**  
* Looker Studio connects directly to the `patek` production table in BigQuery.  
* No local CSVs are required.  
* Directly go to https://lookerstudio.google.com/reporting/cb19f90b-3621-4612-a6a5-d3b467ccbca7.

**2. How to trigger updates:**  
* Run Scenario A (manual pipeline inside the container) to update BigQuery tables.  
* Looker Studio automatically reflects the new data as soon as the `UPDATE` commands finish.  

**3. Result / What the user sees:**  
* Dashboards are always current with the latest data.  
* No refresh button, no local files to manage.  
* Fully automated, end-to-end cloud-native workflow.  

✅ **Notes:**  
* Container exits after pipeline; `--rm` ensures no orphans.  
* Users get instant updates in the dashboard without touching CSVs.  

---

### Summary of Files & Roles

**Project Root:**  
* `Dockerfile` → Defines container environment (Python, dependencies, system tools).  
* `docker-compose.yml` → Orchestrates services, ports, and volumes.  
* `Makefile` → Optional shortcuts to run extraction, FX enrichment, ML, or notebook.  
* `.github/workflows/fx_pipeline.yml` → CI/CD pipeline to update FX rates automatically.  
* `requirements.txt` → Python dependencies.  

**Python Package: `patek_analysis`**  
* `__init__.py` → Marks the folder as a package (keep minimal; no top-level imports).  
* `data.py` → Extraction: downloads raw BigQuery data, cleans it, saves CSV snapshot.  
* `fx_rates.py` → Enrichment: fetches FX rates, writes back to BigQuery, exports CSV.  
* `model.py` → Analytical ML: trains Random Forest on cleaned data, saves predictions.  

**Analysis / Dashboard**  
* `fx_visualization.ipynb` → Notebook for exploratory analysis and visualization.  
* `dashboard/` → `.pbix` file for PowerBI (CSV-based), link to the Looker DB.  

**Secrets / Config**  
* `secrets/` → Place Google service account key here; mounted in container.  

**Key Principle:**  
* Docker ensures reproducibility.  
* Manual or Make commands control execution.  
* CI/CD automates FX enrichment only.  
* ML is optional and downstream; never modifies BigQuery tables automatically.  
