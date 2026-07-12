
from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(

    bootstrap_servers="localhost:9092",

    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

countries = [
    "India",
    "USA",
    "Russia",
    "China",
    "Germany",
    "UK"
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Crypto"
]

devices = [
    "Mobile",
    "Laptop",
    "Unknown"
]

merchants = [
    "Amazon",
    "Flipkart",
    "Binance",
    "Steam",
    "Paytm",
    "Netflix"
]

print("Producer started...")

while True:

    transaction = {

        "user_id": random.randint(1000, 1010),

        "merchant": random.choice(merchants),

        "country": random.choice(countries),

        "payment_method": random.choice(payment_methods),

        "device": random.choice(devices),

        # IMPORTANT FIX
        "amount": round(
            random.uniform(100, 10000),
            2
        )
    }

    producer.send(
        "fraud_topic",
        transaction
    )

    print("Sent:", transaction)

    time.sleep(2)

