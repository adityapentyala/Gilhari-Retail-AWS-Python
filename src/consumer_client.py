from kafka import KafkaConsumer
import json
import requests

BASE_URL = "http://localhost:80/gilhari/v1"

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))
    
def insert_json_data(endpoint, json=None, headers=None, data=None):
    response = requests.post(f'{BASE_URL}/{endpoint}/', data=data, json=json, headers=headers)
    return handle_response(response)

def handle_response(response):
    if response.status_code >= 200 and response.status_code < 300:
        try:
            return response.json()
        except ValueError:
            return response.text
    else:
        response.raise_for_status()

consumer = KafkaConsumer(
    'Employees',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=json_deserializer
)

def consume_stream(uptime):
    consumer = KafkaConsumer(
        'Employees',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=json_deserializer,
        consumer_timeout_ms=uptime*1000
    )
    for message in consumer:
        print(f"{message.value}")
        response = insert_json_data("Employee", json=message.value)
        print(response)
    return None

if __name__ == "__main__":
    consume_stream(100)