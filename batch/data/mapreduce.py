import requests

from collections import defaultdict
from itertools import combinations
from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access.log", 2)

# tell each worker to split each line of its partition
pairs = data.map(lambda line: line.split())

# remove duplicate clicks
pairs = pairs.distinct()

# transform pairs of (user_id, listing_id) into (user_id, Iterable<listing_id>)
pairs = pairs.groupByKey()

# transform (user_id, Iterable<listing_id>) into
# ((listing1, listing2), user_id)
item_pairs = pairs.flatMap(
    lambda pair: [(c, pair[0]) for c in combinations(pair[1], 2)]
)

# tranform ((listing1, listing2), user_id) into
# ((listing1, listing2) Iterable<user_id>)
co_clicks = item_pairs.groupByKey()

# transform ((listing1, listing2), Iterable<user_id>) into
# ((listing1, listing2), len(Iterable<user_id))
co_clicks_count = co_clicks.map(lambda c: (c[0], len(c[1])))

filtered_co_clicks = co_clicks_count.filter(lambda c: c[1] > 2)

# return all elements of dataset as a list
data = filtered_co_clicks.collect()

recommended = defaultdict(list)
# build an undirected graph such that each edge represents a recommendation
for pair, count in data:
    recommended[pair[0]].append(pair[1])
    recommended[pair[1]].append(pair[0])

# reset the database to clear
requests.delete('http://models-api:8000/api/v1/recommendations/')

# post all the recommendations to the database
for key in recommended.keys():
    recs = ','.join(recommended[key])
    data = {'listing_id': key, 'recommended': recs}
    requests.post('http://models-api:8000/api/v1/recommendations/', data=data)

sc.stop()
