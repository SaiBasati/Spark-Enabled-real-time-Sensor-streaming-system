#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import sys
import json
import datetime
import numpy as np
import pprint

from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pymongo_spark
pymongo_spark.activate()
from pyspark.sql import SQLContext


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
        exit(-1)
    

    

    conf = SparkConf().setAppName("pyspark test")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 1)

    zkQuorum, topic, name = sys.argv[1:]

    # Read kafka stream from given topic
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})

    # map first line
    lines = kvs.map(lambda x: x[1])
    # map the line to JSON
    my_parsed_json =  lines.map(lambda x: json.loads(x))

    # filter sensorID and temperature 
    my_rowJSON = my_parsed_json.filter(lambda l: (l['sensorID'] ==  name) and (l['temperature'] >=  50)  ) 
    

    def sendPartition(iter1):
        print(iter1)
        if iter1.count() is not 0:
            iter1.saveToMongoDB('mongodb://localhost:27017/test.spark')
        pass
    
    # iterate through each RDD
    my_rowJSON.foreachRDD(lambda rdd: sendPartition(rdd))   

    ssc.start()
    ssc.awaitTermination()
