from kafka import KafkaConsumer
import json
import requests
import os
from feature_extraction import extract_features

KAFKA_TOPIC = 'ethereum-data'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
ML_BACKEND_PREDICT_URL = 'http://localhost:3000/predict'
FEATURES_FILE = '../data/features.json'

def send_to_ml_backend(features):
    try:
        response = requests.post(ML_BACKEND_PREDICT_URL, json=features)
        response.raise_for_status()
        prediction = response.json()
        print(f"Received prediction for block #{features['blockNumber']}: {prediction}")
        return prediction
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to ML backend for block #{features.get('blockNumber', '?')}: {e}")
        return None


def save_features_to_json(features):
    try:
        if os.path.exists(FEATURES_FILE) and os.path.getsize(FEATURES_FILE) > 0:
            with open(FEATURES_FILE, 'r') as f:
                existing_features = json.load(f)
        else:
            existing_features = []
        existing_features.append(features)
        with open(FEATURES_FILE, 'w') as f:
            json.dump(existing_features, f, indent=2)
    except Exception as e:
        print(f"Error saving features to {FEATURES_FILE}: {e}")

def process_block_data(data):
    print("Received raw data:", data)

    if 'blockNumber' not in data:
        print("Warning: 'blockNumber' key not found in message. Skipping.")
        return

    print(f"\n---------------------\n---------------------\nReceived block data for block #{data['blockNumber']}\n---------------------\n---------------------\n")

    # Extract ML features
    features = extract_features(data)
    print(f"Extracted features: {features}")
    # Save features to a local JSON file
    save_features_to_json(features)
    # Send features to ML backend
    send_to_ml_backend(features)

def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='chainbrain-consumer-group',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    print("Kafka Consumer started - listening to ethereum-data topic ...\n---------------------\n---------------------\n")

    try:
        for message in consumer:
            data = message.value
            process_block_data(data)

    except KeyboardInterrupt:
        print("Consumer stopped by user")

if __name__ == "__main__":
    main()
