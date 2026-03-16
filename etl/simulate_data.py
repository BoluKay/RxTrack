import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Connect to PostgreSQL using credentials from .env
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

fake = Faker()

# --- MEDICATIONS ---
medications = [
    {"name": "Ibuprofen", "category": "Painkiller", "unit": "pills", "reorder_level": 100},
    {"name": "Amoxicillin", "category": "Antibiotic", "unit": "capsules", "reorder_level": 50},
    {"name": "Metformin", "category": "Diabetes", "unit": "pills", "reorder_level": 80},
    {"name": "Lisinopril", "category": "Blood Pressure", "unit": "pills", "reorder_level": 60},
    {"name": "Atorvastatin", "category": "Cholesterol", "unit": "pills", "reorder_level": 70},
    {"name": "Omeprazole", "category": "Antacid", "unit": "capsules", "reorder_level": 90},
    {"name": "Levothyroxine", "category": "Thyroid", "unit": "pills", "reorder_level": 40},
    {"name": "Azithromycin", "category": "Antibiotic", "unit": "tablets", "reorder_level": 30},
    {"name": "Hydrochlorothiazide", "category": "Blood Pressure", "unit": "pills", "reorder_level": 55},
    {"name": "Sertraline", "category": "Antidepressant", "unit": "pills", "reorder_level": 45},
    {"name": "Guanfacine", "category": "ADHD", "unit": "pills", "reorder_level": 40},
    {"name": "Bisolvif Fe", "category": "Contraceptive", "unit": "pills", "reorder_level": 35},
    {"name": "Junel Fe", "category": "Contraceptive", "unit": "pills", "reorder_level": 35},
    {"name": "Adderall XR", "category": "ADHD", "unit": "capsules", "reorder_level": 50},
    {"name": "Cetirizine Hydrochloride", "category": "Antihistamine", "unit": "pills", "reorder_level": 60},
    {"name": "Alprazolam", "category": "Anxiety", "unit": "pills", "reorder_level": 40},
    {"name": "Amlodipine", "category": "Blood Pressure", "unit": "pills", "reorder_level": 60},
    {"name": "Gabapentin", "category": "Nerve Pain", "unit": "capsules", "reorder_level": 55},
    {"name": "Pantoprazole", "category": "Antacid", "unit": "tablets", "reorder_level": 50},
    {"name": "Cyclobenzaprine", "category": "Muscle Relaxant", "unit": "pills", "reorder_level": 35},
    {"name": "Escitalopram", "category": "Antidepressant", "unit": "pills", "reorder_level": 45},
    {"name": "Prednisone", "category": "Steroid", "unit": "pills", "reorder_level": 30},
    {"name": "Tramadol", "category": "Painkiller", "unit": "pills", "reorder_level": 50},
    {"name": "Fluoxetine", "category": "Antidepressant", "unit": "capsules", "reorder_level": 45},
    {"name": "Clonazepam", "category": "Anxiety", "unit": "pills", "reorder_level": 35},
    {"name": "Losartan", "category": "Blood Pressure", "unit": "pills", "reorder_level": 60},
    {"name": "Furosemide", "category": "Diuretic", "unit": "pills", "reorder_level": 40},
    {"name": "Montelukast", "category": "Asthma", "unit": "pills", "reorder_level": 45},
    {"name": "Albuterol", "category": "Asthma", "unit": "inhaler", "reorder_level": 25},
    {"name": "Metoprolol", "category": "Blood Pressure", "unit": "pills", "reorder_level": 55},
    {"name": "Zolpidem", "category": "Sleep Aid", "unit": "pills", "reorder_level": 30},
    {"name": "Doxycycline", "category": "Antibiotic", "unit": "capsules", "reorder_level": 35},
    {"name": "Ciprofloxacin", "category": "Antibiotic", "unit": "tablets", "reorder_level": 40},
    {"name": "Methylphenidate", "category": "ADHD", "unit": "pills", "reorder_level": 45},
    {"name": "Venlafaxine", "category": "Antidepressant", "unit": "capsules", "reorder_level": 40},
    {"name": "Warfarin", "category": "Blood Thinner", "unit": "pills", "reorder_level": 30},
    {"name": "Clopidogrel", "category": "Blood Thinner", "unit": "pills", "reorder_level": 35},
    {"name": "Rosuvastatin", "category": "Cholesterol", "unit": "pills", "reorder_level": 60},
    {"name": "Topiramate", "category": "Seizure", "unit": "pills", "reorder_level": 30},
    {"name": "Lamotrigine", "category": "Seizure", "unit": "pills", "reorder_level": 35},
    {"name": "Quetiapine", "category": "Antipsychotic", "unit": "pills", "reorder_level": 40},
    {"name": "Aripiprazole", "category": "Antipsychotic", "unit": "pills", "reorder_level": 35},
    {"name": "Bupropion", "category": "Antidepressant", "unit": "pills", "reorder_level": 45},
    {"name": "Trazodone", "category": "Sleep Aid", "unit": "pills", "reorder_level": 30},
    {"name": "Hydroxyzine", "category": "Anxiety", "unit": "pills", "reorder_level": 40},
    {"name": "Metronidazole", "category": "Antibiotic", "unit": "tablets", "reorder_level": 35},
    {"name": "Fluconazole", "category": "Antifungal", "unit": "pills", "reorder_level": 25},
    {"name": "Ondansetron", "category": "Nausea", "unit": "pills", "reorder_level": 30},
    {"name": "Famotidine", "category": "Antacid", "unit": "pills", "reorder_level": 45},
    {"name": "Naproxen", "category": "Painkiller", "unit": "pills", "reorder_level": 70},
]

medications_df = pd.DataFrame(medications)

# --- LOAD MEDICATIONS ---
medications_df.to_sql("medications", engine, if_exists="append", index=False)
print("Medications loaded.")

# Fetch medication IDs back from the database
med_df = pd.read_sql("SELECT medication_id, name FROM medications", engine)

# --- INVENTORY ---
inventory_rows = []
locations = ["Shelf A", "Shelf B", "Shelf C", "Storage Room", "Refrigerator"]

for _, row in med_df.iterrows():
    inventory_rows.append({
        "medication_id": row["medication_id"],
        "quantity": np.random.randint(20, 500),
        "location": np.random.choice(locations)
    })

inventory_df = pd.DataFrame(inventory_rows)
inventory_df.to_sql("inventory", engine, if_exists="append", index=False)
print("Inventory loaded.")

# --- SALES ---
sales_rows = []
start_date = datetime.now() - timedelta(days=365)

for _, row in med_df.iterrows():
    for day in range(365):
        sale_date = start_date + timedelta(days=day)
        quantity_sold = max(1, int(np.random.normal(loc=20, scale=5)))
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