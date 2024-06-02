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

def get_attribute_value(endpoint, key, id, attribute):
    """
    Returns the value of the specified attribute of a selected record in the database

    Args:
        endpoint: str - the endpoint (table) to select from
        key: str - the column to select from
        id: Any - the value the key of the record must take (crudely, the row)
        attribute: str - the column whose value in the selected record is to be returned
    
    returns:
        Any, str
    """
    try:
        response = requests.get(f'{BASE_URL}/{endpoint}/getObjectById?filter={key}={id}')
        print(response.json())
        #print(json.loads(response.json)[attribute])
        return (response.json())[attribute]
    except:
        return "null"

def update_attribute_value(endpoint, key, id, attribute, new_value):
    """
    Updates the value of the specified attribute (column) of a selected record in the database

    Args:
        endpoint: str - the endpoint (table) to select from
        key: str - the column to select from
        id: Any - the value the key of the record must take (crudely, the row)
        attribute: str - the column whose value in the selected record is to be updated
        new_value: Any - the value to update the record's attribute with
    
    returns:
        Any
    """
    response = requests.patch(f'{BASE_URL}/{endpoint}?filter={key}={id}', json={"newValues":[attribute, new_value]})
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

def consume_stream(uptime, topics: list[str]):
    """
    Creates a KafkaConsumer to listen to the Kafka stream and adds data to the db using the Gihari API
    Checks for topics and makes requests to the API using the topic as the endpoint

    Args:
        uptime: int - Time in seconds for which consumer should remain active
        topics: list[str] - list of topics to consume
    
    returns:
        None
    """
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=json_deserializer,
        consumer_timeout_ms=uptime*1000
    )
    for message in consumer:
        print(f"{message.value} from {message.topic}")
        if message.topic == "Employees":
            """
            Employee data can be added to the Employee table as-is
            """
            response = insert_json_data("Employees", json=message.value)
            print(response)
        elif message.topic == "Sales":
            """
            A sale can be added to the Sales table as-is, but must also reduce the quantity of the object
            sold in the inventory by the sale quantity
            """
            response = insert_json_data("Sales", json=message.value)
            quantity = get_attribute_value("Inventory", "itemID", message.value["entity"]["itemID"], "quantity")
            response = update_attribute_value("Inventory", "itemID", message.value["entity"]["itemID"], "quantity",
                                              quantity-message.value["entity"]["quantity"])
        elif message.topic == "Inventory":
            """
            Inventory must contain a fixed number of items at its maximum. Hence, transactions cannot be recorded 
            in the Inventory table as-is, but must add to the quantity of a pre-existing item, or create a new 
            item if it does not exist as a record already
            """
            quantity = get_attribute_value("Inventory", "itemID", message.value["entity"]["itemID"], "quantity")
            print(quantity)
            if quantity != "null":
                response = update_attribute_value("Inventory", "itemID", message.value["entity"]["itemID"], "quantity",
                                              quantity+message.value["entity"]["quantity"])
            else:
                response = insert_json_data("Inventory", json=message.value)
    return None

if __name__ == "__main__":
    consume_stream(100, ["Employees", "Sales", "Inventory"])