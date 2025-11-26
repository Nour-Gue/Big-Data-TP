# **Rapport TP7 – Apache Kafka**

## ***1.Installation of Apache Kafka on Windows:***

To start working with Kafka, we installed it on Windows:

1. Downloaded Kafka (version 3.x)
2. Extracted the folder to: `C:\kafka\kafka_2.13-3.4.0`
3. Started  **Zookeeper** : .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
4. Started the main  **Kafka Broker** : .\bin\windows\kafka-server-start.bat .\config\server.properties

**Goal:** Prepare the base Kafka environment (Zookeeper + Broker)

---

## ***2.Creating a Topic:***

1.After Kafka was running, we created our first topic:

bin\windows\kafka-topics.bat --create --topic test-topic --bootstrap-server localhost:9092

2.Check the topics list:

bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092

**Goal:** Create a messaging channel used by producers and consumers

---

## ***3.Producer & Consumer Example (Console):***

We tested Kafka using console tools.

1.Producer (sending messages):

kafka-console-producer.bat --topic test-topic --bootstrap-server localhost:9092

-Example messages:

Hello Kafka!
Message 2

2.Consumer (receiving messages):

kafka-console-consumer.bat --topic test-topic --from-beginning --bootstrap-server localhost:9092

**Goal:** Verify that Kafka can send and receive messages correctly.

---

## ***4.Configuring Multiple Kafka Brokers:***

To create a Kafka  **Cluster** , we added more brokers.

Steps:

1. Copied the default `server.properties` and created:
   * `server-1.properties`
   * `server-2.properties`
2. Edited the configurations:

**Broker 0:**

broker.id=0
listeners=PLAINTEXT://:9092
log.dirs=C:/kafka/.../logs/broker0

**Broker 1:**

broker.id=1
listeners=PLAINTEXT://:9093
log.dirs=C:/kafka/.../logs/broker1

**Broker 2:**

broker.id=2
listeners=PLAINTEXT://:9094
log.dirs=C:/kafka/.../logs/broker2

    3.Started each broker in a separate CMD window:

    kafka-server-start.bat config\server-1.properties
     kafka-server-start.bat config\server-2.properties

**Goal:** Build a Kafka cluster with 3 brokers

---

## ***5.Creating a Replicated Topic:***

We created a topic with **3 partitions** and  **replication factor = 3** :

kafka-topics.bat --create --topic iot-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 3

Then we described it:

kafka-topics.bat --describe --topic iot-topic --bootstrap-server localhost:9092

The output showed:

* Each partition had **3 replicas**
* ISR list included all brokers
* Cluster was working correctly

 **Goal:** Ensure fault tolerance and high availability

---

## ***6.IoT + Kafka Project (Python):***

We built a small IoT simulation using Python.


### **Producer (sensor data generator)**

* Generates temperature and humidity values
* Sends a message every 2 seconds

### **Consumer (receiver)**

* Reads messages from the Kafka cluster
* Prints IoT data in real-time

Commands used:

python consumer.py
python producer.py

Output example:

Sent: {'temperature': 32.1, 'humidity': 55, ...}
Received: {...}

**Goal:** Simulate real IoT device communication using Kafka.
