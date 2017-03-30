


import tweepy #http://www.tweepy.org/
import json
import math
import glob
import csv
from tweepy import TweepError
from time import sleep

from pymongo import MongoClient
connection = c = MongoClient()

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime

# The MongoDB connection info. This assumes your database name is Political and your collection name is tweets.
#connection = Connection('localhost', 27017)
db = connection.Twitter
#db.tweets.ensure_index("id", unique=True, dropDups=True)
#db.tweets.create_index("id", unique=True, dropDups=True)
db.politicians.ensure_index( "id", unique=True, dropDups=True )
collection = db.politicians

new_additions = 0

tweet_count = db.politicians.count("id", exists= True)
print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))

import sys
import os
# Retrieve Twitter API credentials
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv"
with open(twitterKEYfile, 'r') as f:
    e = f.read()
    keys = e.split(',')
    consumer_key = keys[0]  #consumer_key
    consumer_secret = keys[1]  #consumer_secret
    access_key = keys[2]  #access_key
    access_secret = keys[3]  #access_secret
# http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)






# CHANGE THIS TO THE USER YOU WANT
user = 'realdonaldtrump'

#bb#with open('api_keys.json') as f:
#bb#    keys = json.load(f)
#bb#auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
#bb#auth.set_access_token(keys['access_token'], keys['access_token_secret'])
#bb#api = tweepy.API(auth)

user = user.lower()
output_file = '{}.json'.format(user)

with open('all_ids.json') as f:
    ids = json.load(f)

print('total ids: {}'.format(len(ids)))

all_data = []
start = 0
end = 100
limit = len(ids)
i = math.ceil(limit / 100)


#user_json = api.lookup_users(screen_names = ['realdonaldtrump'])
#for a_user in user_json:
#    collection.insert(a_user._json)

for go in range(i):
    print('currently getting {} - {}'.format(start, end))
    sleep(6)  # needed to prevent hitting API rate limit
    id_batch = ids[start:end]
    start += 100
    end += 100
    tweets = api.statuses_lookup(id_batch)
    for tweet in tweets:
        #print (dict(tweet._json))
        one_id = (dict(tweet._json)['id'])
        found = collection.find({'id': one_id}).count()
        if found == 0:
            #print(found)
            #print("inputing tweet to db")
            new_additions += new_additions 
            pass
        #collection.find({'id': 'one_id'})
            all_data.append(dict(tweet._json))
            collection.insert(tweet._json)
        else:
            #print(found)
            #print("Tweet found in db, next")
            pass

        #print('metadata collection complete')
#print('creating master json file')
#with open(output_file, 'w') as outfile:
#    json.dump(all_data, outfile)


results = []

def is_retweet(entry):
    return 'retweeted_status' in entry.keys()

def get_source(entry):
    if '<' in entry["source"]:
        return entry["source"].split('>')[1].split('<')[0]
    else:
        return entry["source"]
        
print ("New additions to DB : " + str(new_additions))
print ("Political db tweet count is : " + str(tweet_count))

#tweet = json.loads(data)
#collection.insert(tweet)
