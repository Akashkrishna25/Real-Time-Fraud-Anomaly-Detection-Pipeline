# from fastapi import FastAPI
# from pydantic import BaseModel
# import sqlite3
# from datetime import datetime
# import pandas as pd

# app = FastAPI()

# # -----------------------------
# # DATABASE CONNECTION
# # -----------------------------

# conn = sqlite3.connect(
#     "fraud.db",
#     check_same_thread=False
# )

# cursor = conn.cursor()

# # -----------------------------
# # CREATE TABLE
# # -----------------------------

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS transactions (

#     id INTEGER PRIMARY KEY AUTOINCREMENT,

#     user_id INTEGER,

#     merchant TEXT,

#     country TEXT,

#     payment_method TEXT,

#     device TEXT,

#     amount REAL,

#     risk_score INTEGER,

#     prediction TEXT,

#     timestamp DATETIME
# )
# """)

# conn.commit()

# # -----------------------------
# # TRANSACTION MODEL
# # -----------------------------

# class Transaction(BaseModel):

#     user_id: int

#     merchant: str

#     country: str

#     payment_method: str

#     device: str

#     Amount: float

# # -----------------------------
# # HOME ROUTE
# # -----------------------------

# @app.get("/")
# def home():

#     return {
#         "message": "Fraud Detection API Running"
#     }

# # -----------------------------
# # PREDICT ROUTE
# # -----------------------------

# @app.post("/predict")
# def predict(transaction: Transaction):

#     data = transaction.dict()

#     risk_score = 0

#     reasons = []

#     # -----------------------------
#     # SUSPICIOUS COUNTRIES
#     # -----------------------------

#     suspicious_countries = [
#         "Russia",
#         "China",
#         "North Korea"
#     ]

#     # -----------------------------
#     # VELOCITY DETECTION
#     # -----------------------------

#     cursor.execute("""
#     SELECT COUNT(*)
#     FROM transactions
#     WHERE user_id = ?
#     AND timestamp >= datetime('now', '-30 seconds')
#     """, (data["user_id"],))

#     velocity = cursor.fetchone()[0]

#     # -----------------------------
#     # FRAUD RULES
#     # -----------------------------

#     # High Amount
#     if data["Amount"] > 5000:

#         risk_score += 30

#         reasons.append(
#             "High Amount Transaction"
#         )

#     # Foreign Country
#     if data["country"] != "India":

#         risk_score += 25

#         reasons.append(
#             "Foreign Country Transaction"
#         )

#     # Crypto Payment
#     if data["payment_method"] == "Crypto":

#         risk_score += 20

#         reasons.append(
#             "Crypto Payment"
#         )

#     # Unknown Device
#     if data["device"] == "Unknown":

#         risk_score += 15

#         reasons.append(
#             "Unknown Device"
#         )

#     # Suspicious Country
#     if data["country"] in suspicious_countries:

#         risk_score += 35

#         reasons.append(
#             "Suspicious Country"
#         )

#     # Rapid Transactions
#     if velocity >= 5:

#         risk_score += 40

#         reasons.append(
#             "Rapid Multiple Transactions"
#         )

#     # -----------------------------
#     # TEMPORARY ML DISABLE
#     # -----------------------------

#     prediction_raw = 1

#     # -----------------------------
#     # FINAL PREDICTION
#     # -----------------------------

#     if risk_score >= 70:

#         prediction = "High Fraud Risk"

#     elif risk_score >= 40:

#         prediction = "Medium Fraud Risk"

#     else:

#         prediction = "Low Fraud Risk"

#     # -----------------------------
#     # SAVE TRANSACTION
#     # -----------------------------

#     cursor.execute("""
#     INSERT INTO transactions (

#         user_id,
#         merchant,
#         country,
#         payment_method,
#         device,
#         amount,
#         risk_score,
#         prediction,
#         timestamp

#     )
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """, (

#         data["user_id"],

#         data["merchant"],

#         data["country"],

#         data["payment_method"],

#         data["device"],

#         data["Amount"],

#         risk_score,

#         prediction,

#         datetime.now()
#     ))

#     conn.commit()

#     # -----------------------------
#     # RESPONSE
#     # -----------------------------

#     return {

#         "prediction": prediction,

#         "risk_score": risk_score,

#         "velocity": velocity,

#         "reasons": reasons,

#         "message": "Fraud analysis complete"
#     }

# @app.get("/transactions")
# def get_transactions():

#     cursor.execute("""
#     SELECT *
#     FROM transactions
#     ORDER BY id DESC
#     LIMIT 50
#     """)

#     rows = cursor.fetchall()

#     data = []

#     for row in rows:

#         data.append({

#             "id": row[0],
#             "user_id": row[1],
#             "merchant": row[2],
#             "country": row[3],
#             "payment_method": row[4],
#             "device": row[5],
#             "amount": row[6],
#             "risk_score": row[7],
#             "prediction": row[8],
#             "timestamp": row[9]
#         })

#     return data

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sqlite3
import os
import joblib
import numpy as np
from pydantic import BaseModel

# -----------------------------------
# FASTAPI APP
# -----------------------------------

app = FastAPI()

# -----------------------------------
# ENABLE CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# DATABASE PATH & SETUP
# -----------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "fraud.db"))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "ml", "fraud_model.pkl"))

# Create table at startup using a single-use connection
with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        merchant TEXT,
        country TEXT,
        payment_method TEXT,
        device TEXT,
        amount REAL,
        risk_score INTEGER,
        prediction TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

# -----------------------------------
# LOAD MODEL
# -----------------------------------
try:
    model = joblib.load(MODEL_PATH)
    print(f"ML Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    model = None
    print(f"Warning: Could not load ML model from {MODEL_PATH}: {e}")

# -----------------------------------
# REQUEST MODEL
# -----------------------------------

class Transaction(BaseModel):

    user_id: int

    merchant: str

    country: str

    payment_method: str

    device: str

    amount: float

# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "Fraud Detection API Running"
    }

# -----------------------------------
# PREDICT ROUTE
# -----------------------------------

@app.post("/predict")
def predict(transaction: Transaction):

    # -----------------------------
    # SIMPLE FEATURE ENGINEERING
    # -----------------------------

    amount = transaction.amount

    risk_score = 0

    # High amount
    if amount > 7000:
        risk_score += 50

    elif amount > 3000:
        risk_score += 30

    # Crypto payment
    if transaction.payment_method == "Crypto":
        risk_score += 30

    # Unknown device
    if transaction.device == "Unknown":
        risk_score += 20

    # Risk countries
    if transaction.country in [
        "Russia",
        "China"
    ]:
        risk_score += 25

    # Clamp score
    risk_score = min(risk_score, 100)

    # --------------------------------
    # PREDICTION LABEL
    # --------------------------------

    if risk_score >= 70:

        prediction = "High Fraud Risk"

    elif risk_score >= 40:

        prediction = "Medium Fraud Risk"

    else:

        prediction = "Safe Transaction"

    # --------------------------------
    # SAVE TO DATABASE
    # --------------------------------

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO transactions (
            user_id,
            merchant,
            country,
            payment_method,
            device,
            amount,
            risk_score,
            prediction
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction.user_id,
            transaction.merchant,
            transaction.country,
            transaction.payment_method,
            transaction.device,
            transaction.amount,
            risk_score,
            prediction
        ))
        conn.commit()

    # --------------------------------
    # RETURN RESPONSE
    # --------------------------------

    return {

        "risk_score": risk_score,

        "prediction": prediction
    }

# -----------------------------------
# GET TRANSACTIONS
# -----------------------------------

@app.get("/transactions")
def get_transactions():

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT *
        FROM transactions
        ORDER BY id DESC
        LIMIT 100
        """)
        rows = cursor.fetchall()

    data = []

    for row in rows:

        data.append({

            "id": row[0],

            "user_id": row[1],

            "merchant": row[2],

            "country": row[3],

            "payment_method": row[4],

            "device": row[5],

            "amount": row[6],

            "risk_score": row[7],

            "prediction": row[8],

            "timestamp": row[9]
        })

    return data