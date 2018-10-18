import os
import requests


def get(model, num):
    url = 'http://models-api:8001/api/v1/{}/{}/'.format(model, num)
    req = requests.get(url)
    req.raise_for_status()
    return req.json()

def post(model,json):
    url = 'http://models-api:8001/api/v1/{}/'.format(model)
    req = requests.post(url, data=json)
    req.raise_for_status()
    # if no exception was raised req was ok

def put(model, num, json):
    url = 'http://models-api:8001/api/v1/{}/{}/'.format(model, num)
    req = requests.put(url, data=json)
    req.raise_for_status()
    # if no exception was raised req was ok

def del(model, num):
    url = 'http://models-api:8001/api/v1/{}/{}/'.format(model, num)
    requests.delete(url)
    req.raise_for_status()
    # if no exception was raised req was ok

def get_all(model):
    url = 'http://models-api:8000/api/v1/{}/'.format(model)
    requests.get(url)
    req.raise_for_status()
    json = req.json['objects']
    return json
