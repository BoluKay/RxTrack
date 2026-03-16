# 💊 RxTrack — Pharmacy Inventory Management System

A full-stack data engineering and machine learning project that tracks pharmacy inventory, predicts stockouts, and alerts on critical shortages.

## Live Demo
![RxTrack Dashboard](docs/dashboard.png)

## Tech Stack
| Layer | Technology |
|---|---|
| Database | PostgreSQL |
| Data Pipeline | Python, pandas, SQLAlchemy |
| Orchestration | Apache Airflow |
| ML Model | scikit-learn (Random Forest) |
| Backend API | FastAPI |
| Frontend | React |

## Features
- **ETL Pipeline** — ingests inventory, sales, and supplier data from multiple sources into a PostgreSQL data warehouse
- **ML Forecasting** — Random Forest model predicts days of stock remaining with 1.36 day MAE and 0.85 R²
- **Real-time API** — FastAPI backend serves inventory data and live ML predictions
- **Interactive Dashboard** — React frontend with shortage alerts, color-coded status indicators, and per-medication forecasts
- **Automated Scheduling** — Apache Airflow DAG runs the pipeline daily

## Project Structure
```
rxtrack/
├── database/        # SQL schema
├── etl/             # ETL pipeline and data simulation
├── ml/              # Model training
├── api/             # FastAPI backend
├── frontend/        # React dashboard
└── airflow/         # Airflow DAG
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/BoluKay/RxTrack.git
cd RxTrack
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the root directory:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rxtrack
DB_USER=postgres
DB_PASSWORD=your_password
```

### 4. Set up the database
```bash
psql -U postgres -c "CREATE DATABASE rxtrack;"
psql -U postgres -d rxtrack -f database/schema.sql
```

### 5. Generate data and run pipeline
```bash
python etl/simulate_data.py
python etl/etl_pipeline.py
```

### 6. Train the model
```bash
python ml/train_model.py
```

### 7. Start the API
```bash
uvicorn api.main:app --reload
```

### 8. Start the frontend
```bash
cd frontend
npm install
npm start
```

Visit **http://localhost:3000**

## Model Performance
- **Mean Absolute Error:** 1.36 days
- **R² Score:** 0.85