from pyspark import SparkContext
from itertools import combinations

# A pseudocode map-reduce style algorithm for computing co-views is
# something like:
#
# Read data in as pairs of (user_id, item_id clicked on by the user)
# Group data into (user_id, list of item ids they clicked on)
# Transform into (user_id, (item1, item2) where item1 and item2 are
# pairs of items the user clicked on
# Transform into ((item1, item2), list of user1, user2 etc) where users
# are all the ones who co-clicked (item1, item2)
# Transform into ((item1, item2), count of distinct users who co-clicked
# (item1, item2)
# Filter out any results where less than 3 users co-clicked the same
# pair of items
# bring the data back to the master node so we can print it out

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access.log", 2)

# tell each worker to split each line of it's partition
pairs = data.map(lambda line: line.split("\t"))


###
# our implementation of algorithm using some spark operations on
# RDD/iter tools

# create dataset of (K, Iterable<V>) pairs
group = pairs.groupByKey()

# map user id to multiple pairs of [user id + item visited]
group_pairs = group.flatMap(lambda items: [(items[0], pair) for pair
                                in combinations(items[1], 2)])

# return all elements of dataset as an array
group_output = group_pairs.collect()

###


# re-layout the data to ignore the user id
pages = pairs.map(lambda pair: (pair[1], 1))

# shuffle the data so that each key is only on one worker
# and then reduce all the values by adding them together
count = pages.reduceByKey(lambda x,y: int(x)+int(y))

output = count.collect()
for page_id, count in output:
    print ("page_id %s count %d" % (page_id, count))
print ("Popular items done")

sc.stop()
