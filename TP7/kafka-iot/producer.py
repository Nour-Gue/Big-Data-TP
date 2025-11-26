from kafka import KafkaProducer
import json
import time
import random


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'iot-topic'

try:
    while True:
      
        data = {
            'temperature': round(random.uniform(20.0, 35.0), 2),
            'humidity': round(random.uniform(30.0, 80.0), 2),
            'timestamp': time.time()
        }
        producer.send(topic, value=data)
        print(f"Sent: {data}")
      
        time.sleep(2)  
except KeyboardInterrupt:
    print("Producer stopped.")
finally:
    producer.close()
