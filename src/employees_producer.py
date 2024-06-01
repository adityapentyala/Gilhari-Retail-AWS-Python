"""
Producer script that sends json data to a Kafka stream for the consumer client to receive
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

    current_time = time.time()
    while current_time-start_time<up_time:
        emp = {"entity":{"id":count, "exempt":random.choice([True, False]), "compensation":random.randint(1,10)*100000, 
               "name":f"emp{count}", "DOB":random.randint(100000,200000)}}
        producer.send("Employees", emp)
        print(emp)
        current_time = time.time()
        count+=1
        time.sleep(random.randint(3,7))
    producer.flush()

    return None

if __name__ == "__main__":
    produce_stream(75, create_producer())