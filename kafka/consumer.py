# from kafka import KafkaConsumer
# import json
# import requests
# import time

# consumer = KafkaConsumer(
#     'transactions',
#     bootstrap_servers='localhost:9092',
#     auto_offset_reset='earliest',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# print("Consumer started...")

# while True:

#     try:

#         for message in consumer:

#             transaction = message.value

#             try:

#                 response = requests.post(
#                     "http://127.0.0.1:8000/predict",
#                     json=transaction,
#                     timeout=5
#                 )

#                 if response.status_code == 200:

#                     result = response.json()

#                     print("\nTransaction Received")
#                     print(transaction)

#                     print("\nPrediction Result")
#                     print(result)

#                 else:

#                     print(f"API Error: {response.status_code}")
#                     print(response.text)

#             except requests.exceptions.ConnectionError:

#                 print("FastAPI server not running on port 8000")

#                 time.sleep(5)

#             except Exception as e:

#                 print("Request Error:", e)

#     except Exception as e:

#         print("Kafka Error:", e)

#         time.sleep(5)


from kafka import KafkaConsumer
import json
import requests

consumer = KafkaConsumer(

    "fraud_topic",

    bootstrap_servers="localhost:9092",

    auto_offset_reset="latest",

    value_deserializer=lambda x: json.loads(
        x.decode("utf-8")
    )
)

print("Consumer started...")

for message in consumer:

    transaction = message.value

    try:

        response = requests.post(

            "http://localhost:8000/predict",

            json=transaction
        )

        print(
            "Prediction:",
            response.json()
        )

    except Exception as e:

        print("API Error:", e)
