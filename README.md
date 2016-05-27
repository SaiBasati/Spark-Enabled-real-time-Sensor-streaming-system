# Spark-Enabled-real-time-Sensor-streaming-system
Spark-Enabled-real-time-Sensor-streaming-system

Demo Video available here:
https://drive.google.com/file/d/0B23R5d_bodtaVHJmN2h4U1VUa28/view?usp=sharing

• Developed a client application to simulate temperature sensor data to Kafka broker

• Setup and deployed Apache Spark locally

• Wrote Spark consumer code to consume streams from Kafka broker

• Filtered data and produce real-time analytics of streaming data.

![ScreenShot](https://cloud.githubusercontent.com/assets/10877598/15622972/744f8fdc-2423-11e6-8241-9009c91c4025.png)

Learning objective: the purpose of this assignment is to design of Web UI (real-time)  that is based Apache Spark based middleware. 

Steps:

1. Download and configure Apache Spark
2. Feed Spark with real-time temperature data (you can create a simple sensor simulator that posts temperature data Apache spark end-point).
3. Process the temperature data on Apache Spark level (RDDs) - apply simple rules such as: temperature greater than 90 implies hot day
4. Stream the values back to WebUI
