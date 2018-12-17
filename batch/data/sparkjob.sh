#!/usr/bin/env bash

# start spark master
bin/spark-class org.apache.spark.deploy.master.Master -h spark-master

# update recommendations every 60 seconds
while true
do
	bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/mapreduce.py
	sleep 60
done
