# Python script to do push cleaned data to our bigquery


from google.cloud import bigquery
import os

# CONFIG
PROJECT = "projectbdm-487109"
DATASET = "patek_data"
ORIGINAL_TABLE = f"{PROJECT}.{DATASET}.patek"
BACKUP_TABLE = f"{PROJECT}.{DATASET}.patek_raw"

def run_migration():
    client = bigquery.Client()
    print("⚙️ Starting Migration...")

    # 1. Create Backup (Copy patek -> patek_raw)
    print(f"1️⃣  Copying data to {BACKUP_TABLE}...")
    sql_backup = f"""
        CREATE OR REPLACE TABLE `{BACKUP_TABLE}` AS
        SELECT * FROM `{ORIGINAL_TABLE}`;
    """
    client.query(sql_backup).result() # Wait for job to finish
    print("   ✅ Backup created.")

    # 2. Overwrite Original with Cleaned Data
    # (Recreates 'patek' using only rows where price is not null)
    print(f"2️⃣  Cleaning {ORIGINAL_TABLE}...")
    sql_clean = f"""
        CREATE OR REPLACE TABLE `{ORIGINAL_TABLE}` AS
        SELECT * FROM `{BACKUP_TABLE}`
        WHERE price IS NOT NULL;
    """
    client.query(sql_clean).result()
    print("   ✅ 'patek' table replaced with cleaned data.")

if __name__ == "__main__":
    run_migration()