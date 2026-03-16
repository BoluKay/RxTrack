from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pandas as pd
import pickle

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Load the trained ML model
with open("ml/model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI(title="RxTrack API", description="Pharmacy Inventory Management System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINT 1: Health check ---
@app.get("/")
def root():
    return {"message": "RxTrack API is running"}

# --- ENDPOINT 2: Get all inventory summary ---
@app.get("/inventory")
def get_inventory():
    df = pd.read_sql("SELECT * FROM inventory_summary", engine)
    return df.to_dict(orient="records")

# --- ENDPOINT 3: Get medications that need reordering ---
@app.get("/alerts")
def get_alerts():
    df = pd.read_sql(
        "SELECT * FROM inventory_summary WHERE needs_reorder = TRUE", engine
    )
    return df.to_dict(orient="records")

# --- ENDPOINT 4: Get forecast for a specific medication ---
@app.get("/forecast/{medication_id}")
def get_forecast(medication_id: int):
    df = pd.read_sql(
        f"SELECT * FROM inventory_summary WHERE medication_id = {medication_id}",
        engine
    )
    if df.empty:
        return {"error": "Medication not found"}
    
    features = df[["current_quantity", "avg_daily_sales", "reorder_level", "lead_time_days"]]
    predicted_days = model.predict(features)[0]
    
    return {
        "medication_id": medication_id,
        "medication_name": df["medication_name"].values[0],
        "current_quantity": int(df["current_quantity"].values[0]),
        "avg_daily_sales": round(float(df["avg_daily_sales"].values[0]), 2),
        "predicted_days_of_stock": round(float(predicted_days), 2),
        "needs_reorder": bool(df["needs_reorder"].values[0])
    }
    
# --- ENDPOINT 5: Get sales history for a medication ---
@app.get("/sales/{medication_id}")
def get_sales_history(medication_id: int):
    df = pd.read_sql(
        f"SELECT sale_date, quantity_sold FROM sales WHERE medication_id = {medication_id} ORDER BY sale_date",
        engine
    )
    if df.empty:
        return []
    df["sale_date"] = df["sale_date"].dt.strftime("%Y-%m-%d")
    return df.to_dict(orient="records")
