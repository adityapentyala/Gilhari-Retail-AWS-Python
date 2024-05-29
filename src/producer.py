from kafka import KafkaProducer
import json
import time

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=json_serializer 
)

with open("data/data.txt", "r") as file:
    textdata = file.readlines()
    file.close()

for i in range(len(textdata)):
    data = {"id":i, "time":time.ctime(time.time()), "text":textdata[i]}
    producer.send("Letters", data)
    print(f"sent {i+1} out of {len(textdata)}")

producer.flush()