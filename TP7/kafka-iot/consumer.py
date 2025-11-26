from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'iot-topic',
    bootstrap_servers='localhost:9092',  
    auto_offset_reset='earliest',         
    group_id='iot-group',               
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Consumer started...")
for message in consumer:
    print(f"Received: {message.value}")
