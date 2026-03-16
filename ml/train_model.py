import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# --- LOAD DATA ---
print("Loading data from inventory_summary...")
df = pd.read_sql("SELECT * FROM inventory_summary", engine)

# --- FEATURES AND TARGET ---
features = ["current_quantity", "avg_daily_sales", "reorder_level", "lead_time_days"]
target = "days_of_stock_remaining"

X = df[features]
y = df[target]

# --- TRAIN/TEST SPLIT ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- TRAIN MODEL ---
print("Training Random Forest model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- EVALUATE ---
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae:.2f} days")
print(f"R² Score: {r2:.2f}")

# --- SAVE MODEL ---
os.makedirs("ml", exist_ok=True)
with open("ml/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved to ml/model.pkl")
print("Training complete.")