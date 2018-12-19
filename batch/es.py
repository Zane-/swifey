import json
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch


with open('db.json') as f:
    fixture = json.load(f)

listings = []
for entry in fixture:
    listings.append(entry['fields'])

consumer = KafkaConsumer(
    'new-listings-topic',
    group_id='listing-indexer',
    bootstrap_servers=['kafka:9092'])

es = Elasticsearch(['es'])

# index fixture data
for i, listing in enumerate(listings):
    es.index(index='listing_index', doc_type='listing', id=i+1, body=listing)
    es.indices.refresh(index="listing_index")

while True:
    for message in consumer:
        new_listing = json.loads((message.value).decode('utf-8'))
        es.index(index='listing_index', doc_type='listing', id=new_listing['id'], body=new_listing)
        es.indices.refresh(index="listing_index")

