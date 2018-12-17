#!/usr/bin/env bash

# install dependencies
apt-get update
apt-get install python3-dev python-pip -y
pip install requests

# update recommendations every 60 seconds
while true
do
	python mapreduce.py
	sleep 60
done
