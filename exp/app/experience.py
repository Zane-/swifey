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

def get_trades(*, for_swipes, sort=None):
    url = 'http://models-api:8000/api/v1/item/'
    requests.get(url)
    req.raise_for_status()
    json = req.json['objects']
    for_swipes_trades = [d for d in objects if d['for_swipes'] == for_swipes]

    if sort == 'high':
        for_swipes_trades.sort(key=lambda d: d['num_swipes'], reverse=True)
    elif sort == 'low':
        for_swipes_trades.sort(key=lambda d: d['num_swipes'])

    return for_swipes_trades
