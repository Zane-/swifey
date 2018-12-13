from pyspark import SparkContext
from itertools import combinations

# A pseudocode map-reduce style algorithm for computing co-views is
# something like:
#
# 1. Read data in as pairs of (user_id, item_id clicked on by the user)
# 2. Group data into (user_id, list of item ids they clicked on)
# 3. Transform into (user_id, (item1, item2) where item1 and item2 are
# pairs of items the user clicked on
# 4. Transform into ((item1, item2), list of user1, user2 etc) where users
# are all the ones who co-clicked (item1, item2)
# 5. Transform into ((item1, item2), count of distinct users who co-clicked
# (item1, item2)
# 6. Filter out any results where less than 3 users co-clicked the same
# pair of items
# 7. bring the data back to the master node so we can print it out

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access.log", 2)

# 1. tell each worker to split each line of it's partition
pairs = data.map(lambda line: line.split("\t"))

# re-layout the data to ignore the user id
pages = pairs.map(lambda pair: (pair[1], 1))

# shuffle the data so that each key is only on one worker
# and then reduce all the values by adding them together
count = pages.reduceByKey(lambda x,y: int(x)+int(y))


###
# our implementation of algorithm using some spark operations on
# RDD/iter tools

# 2. create dataset of (K, Iterable<V>) pairs
group = pairs.groupByKey()

# 3. map user id to multiple pairs of [pair of items visited]
group_pairs = group.flatMap(lambda items: [(items[0], pair) for pair
                                in combinations(items[1], 2)])

# 4. ((item1, item2), list of user1, user2, etc.)
co_clicks = group_pairs.groupByKey()
                        .map(lambda user_list:
                                (user_list[0],
                                    set(user_list[1])))

# 5.
co_clicks_count = co_clicks.map(lambda line: (line[1], len(line[1])))

# 6.
filtered_items = co_clicks_count.filter(lambda users: users[1] > 2)

# return all elements of dataset as an array
output = filtered_items.collect()
###

# output = count.collect()

for page_id, count in output:
    print ("page_id %s count %d" % (page_id, count))
print ("Popular items done")

sc.stop()
