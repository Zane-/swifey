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

def get_all_listings():
    return get_all('listing')

def get_listings(*, listing_type, sort=None):
    listings = [
         d for d in get_all('listing') if d['listing_type'] == listing_type
    ]

    # sort by ascending/descending num_swipes values
    if sort == 'high':
        listings.sort(key=lambda d: d['num_swipes'], reverse=True)
    elif sort == 'low':
        listings.sort(key=lambda d: d['num_swipes'])

    return listings

def signup(post_data):
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

def validate_email(post_data):
    req = requests.post('http://models-api:8000/api/v1/validate_email/', data=post_data)
    if req.status_code == 200:
        return True
    else:
        return False

def create_listing(post_data):
    auth = {
        'user_id': post_data.get('user_id'),
        'authenticator': post_data.get('authenticator'),
        'date_created': post_data.get('auth_date_created')
    }
    authenticated = validate_auth(auth)
    if not authenticated:
        return 'AUTH ERROR'

    data = {
        'user_id': post_data.get('user_id'),
        'title': post_data.get('title'),
        'description': post_data.get('description'),
        'num_swipes': post_data.get('num_swipes'),
        'listing_type': post_data.get('listing_type')
    }
    req = requests.post('http://models-api:8000/api/v1/listing/', data=data)

    if req.status_code == 201:
        data['id'] = int(req.text)
        kafka = KafkaProducer(bootstrap_servers='kafka:9092')
        kafka.send('new-listings-topic', json.dumps(data).encode('utf-8'))
        return int(req.text)
    else:
        return 'FAIL'

def push_to_access_log(user_id, listing_id):
    data = [user_id, listing_id]
    kafka = KafkaProducer(bootstrap_servers='kafka:9092')
    kafka.send('new-recommendations-topic', json.dumps(data).encode('utf-8'))


def get_recommendations(listing_id):
    req = requests.get('http://models-api:8000/api/v1/recommendations/{}/'.format(listing_id))
    if req.status_code == 200:
        return req.json()
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

