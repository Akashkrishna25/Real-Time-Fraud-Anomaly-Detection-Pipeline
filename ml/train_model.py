# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report
# import joblib

# # Load dataset
# data = pd.read_csv("../data/creditcard.csv")

# # Features and target
# X = data.drop("Class", axis=1)
# y = data["Class"]

# # Split dataset
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# # Train model
# model = RandomForestClassifier(n_estimators=50)

# model.fit(X_train, y_train)

# # Predictions
# y_pred = model.predict(X_test)

# # Evaluation
# print(classification_report(y_test, y_pred))

# # Save model
# joblib.dump(model, "fraud_model.pkl")

# print("Model trained and saved successfully")

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import pandas as pd
import joblib

app = FastAPI()

# -----------------------------
# LOAD ML MODEL
# -----------------------------

model = joblib.load("../ml/fraud_model.pkl")

# -----------------------------
# DATABASE
# -----------------------------

conn = sqlite3.connect("fraud.db", check_same_thread=False)

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

    timestamp DATETIME
)
""")

conn.commit()

# -----------------------------
# TRANSACTION MODEL
# -----------------------------

class Transaction(BaseModel):

    user_id: int | None = None

    merchant: str | None = None

    country: str | None = None

    payment_method: str | None = None

    device: str | None = None

    Amount: float

# -----------------------------
# HOME ROUTE
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "AI Fraud Detection API Running"
    }

# -----------------------------
# PREDICT ROUTE
# -----------------------------

@app.post("/predict")
def predict(transaction: Transaction):

    data = transaction.dict()

    risk_score = 0

    # -----------------------------
    # FEATURE ENGINEERING
    # -----------------------------

    country_risk = 1 if data.get("country") in [
        "Russia",
        "China",
        "North Korea"
    ] else 0

    crypto = 1 if data.get(
        "payment_method"
    ) == "Crypto" else 0

    unknown_device = 1 if data.get(
        "device"
    ) == "Unknown" else 0

    # -----------------------------
    # VELOCITY DETECTION
    # -----------------------------

    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    WHERE user_id = ?
    AND timestamp >= datetime('now', '-30 seconds')
    """, (data.get("user_id"),))

    velocity = cursor.fetchone()[0]

    # -----------------------------
    # ML DATAFRAME
    # -----------------------------

    ml_data = pd.DataFrame([{

        "amount": data["Amount"],

        "country_risk": country_risk,

        "crypto": crypto,

        "unknown_device": unknown_device,

        "velocity": velocity
    }])

    # -----------------------------
    # ML PREDICTION
    # -----------------------------

    prediction_raw = model.predict(ml_data)[0]

    if prediction_raw == -1:

        prediction = "Fraud"

        risk_score = 90

    else:

        prediction = "Normal"

        risk_score = 20

    # -----------------------------
    # SAVE TRANSACTION
    # -----------------------------

    cursor.execute("""
    INSERT INTO transactions (

        user_id,
        merchant,
        country,
        payment_method,
        device,
        amount,
        risk_score,
        prediction,
        timestamp

    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        data.get("user_id"),

        data.get("merchant", "Unknown"),

        data.get("country", "India"),

        data.get("payment_method", "UPI"),

        data.get("device", "Mobile"),

        data["Amount"],

        risk_score,

        prediction,

        datetime.now()
    ))

    conn.commit()

    return {

        "prediction": prediction,

        "risk_score": risk_score,

        "velocity": velocity,

        "message": "AI fraud analysis complete"
    }