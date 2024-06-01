"""
Consumer script that receives data as bytes from Kafka stream, converts back to json, and POSTs requests to 
add json data to a db using Gilhari API
"""
from kafka import KafkaConsumer
import json
import requests

BASE_URL = "http://localhost:80/gilhari/v1"

def json_deserializer(data):
    """
    Converts bytes data from stream back to json

    Args:
        data: bytes - consumer message value to be converted to json
    
    returns:
        dict
    """
    return json.loads(data.decode('utf-8'))
    
def insert_json_data(endpoint, json=None, headers=None, data=None):
    """
    Creates POST request to API endpoint to add new entity to database

    Args:
        json: dict[str, dict[str, Any]] - entity to be added to the db. Defaults to None.
        headers: _HeadersMapping - placeholder argument. Defaults to None.
        data: _Data - placeholder argument. Defaults to None.
    
    returns:
        Any
    """
    response = requests.post(f'{BASE_URL}/{endpoint}/', data=data, json=json, headers=headers)
    return handle_response(response)

def handle_response(response):
    """
    Handles response received from API request

    Args:
        response: Response - response received from the API
    
    returns:
        Any
    """
    if response.status_code >= 200 and response.status_code < 300:
        try:
            return response.json()
        except ValueError:
            return response.text
    else:
        response.raise_for_status()

def consume_stream(uptime):
    """
    Creates a KafkaConsumer to listen to the Kafka stream and adds data to the db using the Gihari API

    Args:
        uptime: int - Time in seconds for which consumer should remain active
    
    returns:
        None
    """
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