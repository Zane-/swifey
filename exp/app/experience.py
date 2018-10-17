import os
import requests

os.environ['NO_PROXY'] = '127.0.0.1'

def get(model, num):
    url = 'http://127.0.0.1:8001/api/v1/{}/{}/'.format(model, num)
    req = requests.get(url)
    req.raise_for_status()
    return req.json()

def post(model,json):
    url = 'http://127.0.0.1:8001/api/v1/{}/'.format(model)
    req = requests.post(url, data=json)
    req.raise_for_status()
    # if no exception was raised req was ok
    return 'OK'

def put(model, num, json):
    url = 'http://127.0.0.1:8001/api/v1/{}/{}/'.format(model, num)
    req = requests.put(url, data=json)
    req.raise_for_status()
    # if no exception was raised req was ok
    return 'OK'

def del(model, num):
    url = 'http://127.0.0.1:8001/api/v1/{}/{}/'.format(model, num)
    requests.delete(url)
    req.raise_for_status()
    # if no exception was raised req was ok
    return 'OK'
