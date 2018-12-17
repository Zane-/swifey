#!/usr/bin/env bash

# install dependencies
apt-get update
apt-get install python3-dev python-pip -y
pip install requests

# update recommendations every 60 seconds
while true
do
	sleep 60
	/bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/mapreduce.py
done
