import requests

from collections import defaultdict
from itertools import combinations
from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access.log", 2)

# tell each worker to split each line of its partition
pairs = data.map(lambda line: tuple(line.split()))

# remove duplicate clicks
pairs = pairs.distinct()
# transform pairs of (user_id, listing_id) into (user_id, Iterable<listing_id>)
group_pairs = pairs.groupByKey()

# transform (user_id, Iterable<listing_id>) into
# ((listing1, listing2), user_id)
# we sort the list of listing ids clicked so we don't end
# up with something like (6, 1) -> (1, 6) for different user ids
# as these would not count as a co-click
item_pairs = group_pairs.flatMap(
    lambda pair: ((c, pair[0]) for c in combinations(sorted(pair[1]), 2))
)
# tranform ((listing1, listing2), user_id) into
# ((listing1, listing2), Iterable<user_id>)
co_clicks = item_pairs.groupByKey()
#
# # filter out co_clicks with length less than 3
filtered_co_clicks = co_clicks.filter(lambda c: len(c[1]) > 2)

# return all elements of dataset as a list
output = filtered_co_clicks.collect()

recommended = defaultdict(set)
# build an undirected graph such that each edge represents a recommendation
for pair, count in output:
    recommended[pair[0]].add(pair[1])
    recommended[pair[1]].add(pair[0])

# reset the recommendations database
requests.delete('http://models-api:8000/api/v1/recommendations/')

# post all the recommendations to the database
for key in recommended.keys():
    recs = ','.join(recommended[key])
    data = {'listing_id': key, 'recommended': recs}
    requests.post('http://models-api:8000/api/v1/recommendations/', data=data)

sc.stop()
