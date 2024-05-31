# Setting up Gilhari microservice
Proceed to `/java_src/README.md` and follow the instructions there

# Setting up project environment
Follow these steps to set up your dev/testing environment

### Step 1: Install Python 3.10
Install python 3.10 from official sources. Ensure you are using python 3.10 by running the command `python --version`

### Step 2: Cloning repository and setting up virtual environment
Clone this repository and navigate to the root of your local repository in a terminal. Then, run the command `python -m venv gilhari-kafka-env`

Activate the environment by running the command:

`gilhari-kafka-env/Scripts/activate.bat` (Windows command prompt)

`gilhari-kafka-env/Scripts/activate.ps1` (Windows powershell)

`source gilhari-kafka-env/bin/activate` (MacOS/Linux)

### Step 3: Install requirements from requirements.txt
run the command `pip install -r requirements.txt` after activating the virtual environment

verify installation by running the command `pip list`

# Setting up Kafka data streaming server
Navigate to your kafka directory (eg, home/usr/kafka_2.13-3.7.0) and run the following commands in separate terminals

## Start zookeeper server (default port 2181)
run the command `bin/zookeeper-server-start.sh config/zookeeper.properties`

## Start kafka server (default port 9092)
run the command `bin/kafka-server-start.sh config/server.properties`

## Stopping the servers
run the commands

`bin/kafka-server-stop.sh`

`bin/zookeeper-server-stop.sh`

# Running the project
Follow the above steps to set up both servers. Then in a new terminal located in the root directory of the project, proceed to the following:

## Generate data using a producer application
run the command `python producer.py`

## Retrieving json data using the consumer
run the command `python consumer_client.py`
