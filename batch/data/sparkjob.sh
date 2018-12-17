#!/usr/bin/env bash

# install dependencies
apt-get update
apt-get install python3-dev default-libmysqlclient-dev python-pip python-mysqldb -y
pip install mysqlclient

# update recommendations every 60 seconds
while true
do
	python mapreduce.py
	sleep 60
done
