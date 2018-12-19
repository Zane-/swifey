import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'new-recommendations-topic',
    group_id='recommendation-indexer',
    bootstrap_servers=['kafka:9092']
)

while True:
    for message in consumer:
        data = json.loads((message.value).decode('utf-8'))
        # append line to access log -> user_id listing_id
        with open('data/access.log', 'a+') as f:
            f.write('{} {}\n'.format(data[0], data[1]))
