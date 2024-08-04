# Creating the Project-Specific Gilhari Image
This file lists out the steps taken to configure the Gilhari microservice along with JDX ORM. In this example, the classes named Employee, InventoryItem and Sale are created and mapped as follows.

## Step 1. Define and compile empty Java (container) class
To use Gilhari, we first define empty Java (container) classes for each conceptual type of the JSON objects (domain model classes) used in our application.

This example uses 3 object classes with the following attributes -
* JSON_Employee
    * id (Long) (PRIMARY KEY)
    * name (String)
    * exempt (Boolean)
    * compensation (Double)
    * DOB (Long)
* JSON_Sale 
    * id (Long) (PRIMARY KEY)
    * itemID (Long) 
    * itemName (String)
    * quantity (Double)
    * date (Long)
* JSON_InventoryItem
    * itemID (Long)
    * itemName (String)
    * quantity (Double)
    * date (Long)

Now we compile the previously defined empty domain model classes as follows:

In `src/main/java/models`, create a class file `JSON_Employee.java` as shown to create a JDX_JSONObject (derived from Software Tree's JDX).\
Similarly, create class files `JSON_InventoryItem.java` and `JSON_Sale.java` in the same location.\
In the `lib/` directory, add the requirements as `.jar` files (here, a json package and `jxclasses.jar`, found in the `libs/` directory of the Gilhari SDK installation).\
In a terminal, `cd` to `Gilhari9/` and run the command `javac -cp "lib/json-20240303.jar:lib/jxclasses.jar" -d bin src/main/java/models/JSON_Employee.java`. Repeat the same for the other 2 files.

## Step 2. Define a declarative Object Relational Mapping (ORM) specification and Gilhari configuration
Now we define a declarative Object Relational Mapping (ORM) specification on those domain model classes mapping attributes of the conceptual JSON objects to the corresponding relational artifacts. The ORM file also contains details about the databse system in use (PostgreSQL/MySQL/SQLite). The steps to create and configure the ORM specification and Gilhari configuration are as follows:

In `config/`, create a file named `gilhari9_sqlite3.jdx` as shown. (This example uses an SQLite database, but can be quickly modified to support a MySQL or PostgreSQL database instead).\
Also add to `config/` the database's (here, postgresql's) JDBC driver as a `.jar`.\
Add a file `classNameMapping.js` to `config/` to map "Employees" to the defined Employee container class. Repeat the same for the other 2 classes as shown.\
Finally, to `Gilhari9/`, add a file `gilhari_service.config` and fill in the required fields. Refer to the Gilhari documentation for more information on the `.config` file and its fields.

## Step 3. Create a Dockerfile, build and run the container
Create the Dockerfile as shown and run the command
`docker build -t my_app_gilhari -f ./Dockerfile .` to build the docker image.\

### Using SQLite Database
If using an SQLite database, you may run the container using the command `docker run -p 80:8081 -v /<PROJECT-DIRECTORY>/Gilhari9/config:/opt/gilhariresolverexample/config my_app_gilhari`, where `PROJECT-DIRECTORY` is the absolute path to this project's directory on your system. This ensures that changes made to SQLite's `.db` file will persist after the container is stopped.

### Using MySQL/PostgreSQL database
Simply run the container using the command `docker run -p 80:8081 my_app_gilhari`

