# Producer (send test message)
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

producer.send('ethereum-data', {"msg": "Hello from Kafka!"})
producer.flush()
print("Test message sent!")