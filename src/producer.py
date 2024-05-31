from kafka import KafkaProducer
import json
import time
import random

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=json_serializer 
)

def produce_stream(up_time):
    count=2
    time.sleep(4)
    start_time = time.time()

    current_time = time.time()
    while current_time-start_time<up_time:
        emp = {"entity":{"id":count, "exempt":random.choice([True, False]), "compensation":random.randint(1,10)*100000, 
               "name":f"emp{count}", "DOB":random.randint(100000,200000)}}
        producer.send("Employees", emp)
        current_time = time.time()
        count+=1
        time.sleep(random.randint(3,7))
    producer.flush()

    return None

if __name__ == "__main__":
    produce_stream(75)