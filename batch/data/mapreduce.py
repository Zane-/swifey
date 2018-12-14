import MySQLdb

from pyspark import SparkContext
from itertools import combinations

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
output = filtered_co_clicks.collect()

db = MySQLdb.connect(host="db", user="www", passwd="$3cureUS", db="cs4501")
# SQL query to clear the recommendation table
# take each pair of (listing1, listing2) and add
# listing2 to listing1's recommendations and listing 1 to listing2's recommendations
for pair, count in output:
    db.query()

sc.stop()
