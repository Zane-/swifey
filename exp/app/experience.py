import json
import os
import requests

from django.contrib.auth.hashers import make_password
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

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
    return 'OK'

def put(model, num, json):
    url = 'http://models-api:8000/api/v1/{}/{}/update/'.format(model, num)
    req = requests.put(url, data=json)
    req.raise_for_status()
    # if no exception was raised req was ok
    return 'OK'

def delete(model, num):
    url = 'http://models-api:8000/api/v1/{}/{}/'.format(model, num)
    req = requests.delete(url)
    req.raise_for_status()
    # if no exception was raised req was ok
    return 'OK'

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

def signup(post_data):
    post_data = post_data.copy()
    post_data['password'] = make_password(post_data['password'])
    req = requests.post('http://models-api:8000/api/v1/user/', data=post_data)
    if req.status_code == 201:
        # return the auth token if user successfully signs up
        return login(post_data)
    else:
        # form did not validate
        return 'FAIL'

def login(post_data):
    req = requests.post('http://models-api:8000/api/v1/login/', data=post_data)
    if req.status_code not in (400, 401):
        # auth containing user_id and auth token
        return req.json()
    else:
        return 'FAIL'

def validate_auth(post_data):
    if post_data is None:
        return False

    req = requests.post('http://models-api:8000/api/v1/auth/', data=post_data)
    if req.status_code == 200:
        return True
    else:
        return False

def validate_email(email):
    req = requests.post('http://models-api:8000/api/v1/validate_email/', data=email)
    if req.status_code == 200:
        return True
    else:
        return False

def create_listing(post_data):
    auth = post_data['auth']
    valid = validate_auth(auth)
    if not valid:
        return 'AUTH ERROR'

    data = {
        'title': post_data['title'],
        'description': post_data['description'],
        'num_swipes': post_data['num_swipes'],
         'listing_type': post_data['listing_type']
    }
    req = requests.post('http://models-api:8000/api/v1/listing/', data=post_data)
    if req.status_code == 201:
        data['id'] = int(req.text)
        kafka = KafkaProducer(bootstrap_servers='kafka:9092')
        kafka.send('new-listings-topic', json.dumps(data).encode('utf-8'))
        return 'OK'
    else:
        return 'FAIL'

def search(query):
    es = Elasticsearch(['es'])
    results = es.search(
        index='listing_index',
        body={
            'query':{
                'query_string': {
                    'query': query
                },
            },
            'size': 10,
        }
    )
    hits = results['hits']['hits']
    listings = []
    for hit in hits:
        data = {
            'score': hit['_score'],
            'listing': hit['_source'],
        }
        listings.append(data)
    # sort from high score to low score
    listings.sort(key=lambda listing: listing['score'], reverse=True)
    # remove scores as they are not needed by the front-end
    # after we sort them
    listings = [listing['listing'] for listing in listings]
    return listings
