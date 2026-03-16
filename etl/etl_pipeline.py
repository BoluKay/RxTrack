import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# --- EXTRACT ---
print("Extracting data...")

medications_df = pd.read_sql("SELECT * FROM medications", engine)
inventory_df = pd.read_sql("SELECT * FROM inventory", engine)
sales_df = pd.read_sql("SELECT * FROM sales", engine)
suppliers_df = pd.read_sql("SELECT * FROM suppliers", engine)

print("Extraction complete.")

# --- TRANSFORM ---
print("Transforming data...")

# Calculate average daily sales per medication
avg_sales = sales_df.groupby("medication_id")["quantity_sold"].mean().reset_index()
avg_sales.columns = ["medication_id", "avg_daily_sales"]

# Get latest inventory quantity per medication
latest_inventory = inventory_df[["medication_id", "quantity"]].copy()
latest_inventory.columns = ["medication_id", "current_quantity"]

# Get lead time from suppliers
lead_times = suppliers_df[["medication_id", "lead_time_days"]]

# Join everything together
summary = medications_df[["medication_id", "name", "category", "reorder_level"]].merge(latest_inventory, on="medication_id")
summary = summary.merge(avg_sales, on="medication_id")
summary = summary.merge(lead_times, on="medication_id")

# Calculate days of stock remaining
summary["days_of_stock_remaining"] = summary["current_quantity"] / summary["avg_daily_sales"]

# Flag medications that need reordering
summary["needs_reorder"] = summary["current_quantity"] <= summary["reorder_level"]

# Rename name column
summary = summary.rename(columns={"name": "medication_name"})

print("Transformation complete.")

# --- LOAD ---
print("Loading into inventory_summary...")

# Drop existing summary data and reload fresh
with engine.connect() as conn:
    conn.execute(__import__('sqlalchemy').text("DELETE FROM inventory_summary"))
    conn.commit()

summary_to_load = summary[[
    "medication_id",
    "medication_name",
    "category",
    "current_quantity",
    "avg_daily_sales",
    "days_of_stock_remaining",
    "reorder_level",
    "lead_time_days",
    "needs_reorder"
]]

summary_to_load.to_sql("inventory_summary", engine, if_exists="append", index=False)

print("Load complete.")
print("ETL pipeline finished successfully.")