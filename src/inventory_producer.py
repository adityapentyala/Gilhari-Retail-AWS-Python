"""
Producer script that sends json data to a Kafka stream for the consumer client to receive. This particular script
sends shipment-related data - that is, additions to inventory
"""
from kafka import KafkaProducer
import json
import time
import random

def json_serializer(data):
    """
    Function to serialize and encode json data as binary

    Args:
        data: dict[str, Any] - json data to be encoded
    
    returns:
        bytes
    """
    return json.dumps(data).encode('utf-8')

def create_producer():
    """
    Creates a producer for use
    """
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=json_serializer 
    )
    return producer

def produce_stream(up_time, producer):
    """
    Function that uses previously defined KafkaProducer to send data to the streaming service. Function
    takes one argument to generate data for a set number of seconds, sending a datapoint every 3-7 seconds

    Args:
        up_time: int - time in seconds during which producer must send data
        producer: KafkaProducer

    returns:
        None
    """
    count=2
    time.sleep(4)
    start_time = time.time()
    sample_items = ["Apples", "Bananas", "Pears", "Strawberries", "Cherries", "Kiwi", "Orange", "Watermelon"]
    current_time = time.time()
    while current_time-start_time<up_time:
        choice = random.randint(0, len(sample_items)-1)
        item = {"entity":{"quantity":random.randint(1,5)*25, "date":int(time.time()),
                          "itemName":sample_items[choice], "itemID":choice}}
        producer.send("Inventory", item)
        print(item)
        current_time = time.time()
        count+=1
        time.sleep(random.randint(3,7))
    producer.flush()

    return None

if __name__ == "__main__":
    produce_stream(75, create_producer())