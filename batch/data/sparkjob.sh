#!/usr/bin/env bash

# start spark master
bin/spark-class org.apache.spark.deploy.master.Master -h spark-master &

# install dependencies
apt-get update && apt-get install python3-dev python-pip -y
pip install requests

# update recommendations every 60 seconds
while true
do
	bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/mapreduce.py
	sleep 60
done
