import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

fake = Faker()

medications = [
    {"name": "Ibuprofen", "category": "Painkiller", "unit": "pills", "reorder_level": 500},
    {"name": "Amoxicillin", "category": "Antibiotic", "unit": "capsules", "reorder_level": 200},
    {"name": "Metformin", "category": "Diabetes", "unit": "pills", "reorder_level": 300},
    {"name": "Lisinopril", "category": "Blood Pressure", "unit": "pills", "reorder_level": 250},
    {"name": "Atorvastatin", "category": "Cholesterol", "unit": "pills", "reorder_level": 200},
    {"name": "Omeprazole", "category": "Antacid", "unit": "capsules", "reorder_level": 350},
    {"name": "Levothyroxine", "category": "Thyroid", "unit": "pills", "reorder_level": 150},
    {"name": "Azithromycin", "category": "Antibiotic", "unit": "tablets", "reorder_level": 200},
    {"name": "Hydrochlorothiazide", "category": "Blood Pressure", "unit": "pills", "reorder_level": 250},
    {"name": "Sertraline", "category": "Antidepressant", "unit": "pills", "reorder_level": 150},
    {"name": "Guanfacine", "category": "ADHD", "unit": "pills", "reorder_level": 100},
    {"name": "Bisolvif Fe", "category": "Contraceptive", "unit": "pills", "reorder_level": 80},
    {"name": "Junel Fe", "category": "Contraceptive", "unit": "pills", "reorder_level": 80},
    {"name": "Adderall XR", "category": "ADHD", "unit": "capsules", "reorder_level": 100},
    {"name": "Cetirizine Hydrochloride", "category": "Antihistamine", "unit": "pills", "reorder_level": 300},
    {"name": "Alprazolam", "category": "Anxiety", "unit": "pills", "reorder_level": 120},
    {"name": "Amlodipine", "category": "Blood Pressure", "unit": "pills", "reorder_level": 250},
    {"name": "Gabapentin", "category": "Nerve Pain", "unit": "capsules", "reorder_level": 120},
    {"name": "Pantoprazole", "category": "Antacid", "unit": "tablets", "reorder_level": 350},
    {"name": "Cyclobenzaprine", "category": "Muscle Relaxant", "unit": "pills", "reorder_level": 100},
    {"name": "Escitalopram", "category": "Antidepressant", "unit": "pills", "reorder_level": 150},
    {"name": "Prednisone", "category": "Steroid", "unit": "pills", "reorder_level": 80},
    {"name": "Tramadol", "category": "Painkiller", "unit": "pills", "reorder_level": 500},
    {"name": "Fluoxetine", "category": "Antidepressant", "unit": "capsules", "reorder_level": 150},
    {"name": "Clonazepam", "category": "Anxiety", "unit": "pills", "reorder_level": 120},
    {"name": "Losartan", "category": "Blood Pressure", "unit": "pills", "reorder_level": 250},
    {"name": "Furosemide", "category": "Diuretic", "unit": "pills", "reorder_level": 150},
    {"name": "Montelukast", "category": "Asthma", "unit": "pills", "reorder_level": 180},
    {"name": "Albuterol", "category": "Asthma", "unit": "inhaler", "reorder_level": 180},
    {"name": "Metoprolol", "category": "Blood Pressure", "unit": "pills", "reorder_level": 250},
    {"name": "Zolpidem", "category": "Sleep Aid", "unit": "pills", "reorder_level": 100},
    {"name": "Doxycycline", "category": "Antibiotic", "unit": "capsules", "reorder_level": 200},
    {"name": "Ciprofloxacin", "category": "Antibiotic", "unit": "tablets", "reorder_level": 200},
    {"name": "Methylphenidate", "category": "ADHD", "unit": "pills", "reorder_level": 100},
    {"name": "Venlafaxine", "category": "Antidepressant", "unit": "capsules", "reorder_level": 150},
    {"name": "Warfarin", "category": "Blood Thinner", "unit": "pills", "reorder_level": 120},
    {"name": "Clopidogrel", "category": "Blood Thinner", "unit": "pills", "reorder_level": 120},
    {"name": "Rosuvastatin", "category": "Cholesterol", "unit": "pills", "reorder_level": 200},
    {"name": "Topiramate", "category": "Seizure", "unit": "pills", "reorder_level": 70},
    {"name": "Lamotrigine", "category": "Seizure", "unit": "pills", "reorder_level": 70},
    {"name": "Quetiapine", "category": "Antipsychotic", "unit": "pills", "reorder_level": 70},
    {"name": "Aripiprazole", "category": "Antipsychotic", "unit": "pills", "reorder_level": 70},
    {"name": "Bupropion", "category": "Antidepressant", "unit": "pills", "reorder_level": 150},
    {"name": "Trazodone", "category": "Sleep Aid", "unit": "pills", "reorder_level": 100},
    {"name": "Hydroxyzine", "category": "Anxiety", "unit": "pills", "reorder_level": 120},
    {"name": "Metronidazole", "category": "Antibiotic", "unit": "tablets", "reorder_level": 200},
    {"name": "Fluconazole", "category": "Antifungal", "unit": "pills", "reorder_level": 50},
    {"name": "Ondansetron", "category": "Nausea", "unit": "pills", "reorder_level": 80},
    {"name": "Famotidine", "category": "Antacid", "unit": "pills", "reorder_level": 350},
    {"name": "Naproxen", "category": "Painkiller", "unit": "pills", "reorder_level": 500},
]

sales_profiles = {
    "Painkiller": {"mean": 120, "std": 20},
    "Antibiotic": {"mean": 45, "std": 10},
    "Diabetes": {"mean": 80, "std": 12},
    "Blood Pressure": {"mean": 70, "std": 10},
    "Cholesterol": {"mean": 60, "std": 8},
    "Antacid": {"mean": 90, "std": 15},
    "Thyroid": {"mean": 50, "std": 8},
    "Antidepressant": {"mean": 40, "std": 8},
    "Anxiety": {"mean": 35, "std": 7},
    "ADHD": {"mean": 30, "std": 6},
    "Contraceptive": {"mean": 25, "std": 5},
    "Antihistamine": {"mean": 85, "std": 15},
    "Nerve Pain": {"mean": 35, "std": 7},
    "Muscle Relaxant": {"mean": 30, "std": 6},
    "Steroid": {"mean": 25, "std": 5},
    "Diuretic": {"mean": 40, "std": 8},
    "Asthma": {"mean": 45, "std": 9},
    "Sleep Aid": {"mean": 30, "std": 6},
    "Blood Thinner": {"mean": 35, "std": 7},
    "Seizure": {"mean": 20, "std": 4},
    "Antipsychotic": {"mean": 20, "std": 4},
    "Antifungal": {"mean": 15, "std": 3},
    "Nausea": {"mean": 25, "std": 5},
}

seasonal_multipliers = {
    "Antihistamine": {3: 1.4, 4: 1.6, 5: 1.5, 9: 1.3, 10: 1.2},
    "Asthma": {3: 1.3, 4: 1.4, 9: 1.3, 10: 1.2},
    "Antibiotic": {11: 1.3, 12: 1.5, 1: 1.5, 2: 1.4},
    "Painkiller": {11: 1.2, 12: 1.3, 1: 1.2},
}

medications_df = pd.DataFrame(medications)
medications_df.to_sql("medications", engine, if_exists="append", index=False)
print("Medications loaded.")

med_df = pd.read_sql("SELECT medication_id, name FROM medications", engine)

# Build category map
med_cat_map = {}
for _, row in med_df.iterrows():
    match = next((m for m in medications if m["name"] == row["name"]), None)
    if match:
        med_cat_map[row["medication_id"]] = match["category"]

# --- INVENTORY ---
inventory_rows = []
locations = ["Shelf A", "Shelf B", "Shelf C", "Storage Room", "Refrigerator"]

for _, row in med_df.iterrows():
    category = med_cat_map.get(row["medication_id"], "Painkiller")
    profile = sales_profiles.get(category, {"mean": 30, "std": 6})
    daily_sales = profile["mean"]
    days_of_stock = np.random.randint(10, 45)
    starting_quantity = max(50, int(daily_sales * days_of_stock))
    inventory_rows.append({
        "medication_id": row["medication_id"],
        "quantity": starting_quantity,
        "location": np.random.choice(locations)
    })

inventory_df = pd.DataFrame(inventory_rows)
inventory_df.to_sql("inventory", engine, if_exists="append", index=False)
print("Inventory loaded.")

# --- SALES ---
sales_rows = []
start_date = datetime.now() - timedelta(days=365)

for _, row in med_df.iterrows():
    category = med_cat_map.get(row["medication_id"], "Painkiller")
    profile = sales_profiles.get(category, {"mean": 30, "std": 6})
    season = seasonal_multipliers.get(category, {})

    for day in range(365):
        sale_date = start_date + timedelta(days=day)
        month = sale_date.month
        multiplier = season.get(month, 1.0)
        mean_sales = profile["mean"] * multiplier
        quantity_sold = max(1, int(np.random.normal(loc=mean_sales, scale=profile["std"])))
        sales_rows.append({
            "medication_id": row["medication_id"],
            "quantity_sold": quantity_sold,
            "sale_date": sale_date
        })

sales_df = pd.DataFrame(sales_rows)
sales_df.to_sql("sales", engine, if_exists="append", index=False)
print("Sales loaded.")

# --- SUPPLIERS ---
supplier_names = [
    "MedSupply Co", "PharmaDist Inc", "RxSource LLC",
    "NationalMeds", "QuickPharm Distributors"
]

supplier_rows = []
for _, row in med_df.iterrows():
    supplier_rows.append({
        "medication_id": row["medication_id"],
        "supplier_name": np.random.choice(supplier_names),
        "lead_time_days": np.random.randint(2, 14),
        "last_order_date": fake.date_between(start_date="-90d", end_date="today")
    })

suppliers_df = pd.DataFrame(supplier_rows)
suppliers_df.to_sql("suppliers", engine, if_exists="append", index=False)
print("Suppliers loaded.")

print("All data loaded successfully into RxTrack database.")