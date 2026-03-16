-- RxTrack Database Schema
-- Pharmacy Inventory Management System

CREATE TABLE medications (
    medication_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    unit VARCHAR(50),
    reorder_level INT NOT NULL
);

CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    medication_id INT REFERENCES medications(medication_id),
    quantity INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(100)
);

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    medication_id INT REFERENCES medications(medication_id),
    quantity_sold INT NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    medication_id INT REFERENCES medications(medication_id),
    supplier_name VARCHAR(255) NOT NULL,
    lead_time_days INT NOT NULL,
    last_order_date DATE
);