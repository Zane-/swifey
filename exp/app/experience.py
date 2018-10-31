import os
import requests

os.environ['NO_PROXY'] = '127.0.0.1'

def get(model, num):
    url = 'http://models-api:8000/api/v1/{}/{}/'.format(model, num)
    req = requests.get(url)
    req.raise_for_status()
    return req.json()

def post(model,json):
    url = 'http://models-api:8000/api/v1/{}/'.format(model)
    req = requests.post(url, data=json)
    req.raise_for_status()
    # if no exception was raised req was ok

def put(model, num, json):
    url = 'http://models-api:8000/api/v1/{}/{}/'.format(model, num)
    req = requests.put(url, data=json)
    req.raise_for_status()
    # if no exception was raised req was ok

def delete(model, num):
    url = 'http://models-api:8000/api/v1/{}/{}/'.format(model, num)
    req = requests.delete(url)
    req.raise_for_status()
    # if no exception was raised req was ok

def get_all(model):
    url = 'http://models-api:8000/api/v1/{}/'.format(model)
    req = requests.get(url)
    req.raise_for_status()
    json = req.json()
    return json

def get_listings(*, listing_type, sort=None):
    trades = [
         d for d in get_all('listing') if d['listing_type'] == listing_type
    ]

    # sort by ascending/descending num_swipes values
    if sort == 'high':
        trades.sort(key=lambda d: d['num_swipes'], reverse=True)
    elif sort == 'low':
        trades.sort(key=lambda d: d['num_swipes'])

    return trades

