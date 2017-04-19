#!/usr/bin/python
# cd /mnt/8TB/GITS/twitter_scraping
# python3 twitter_DB_update_tweets_metadata.py

# Retrieves tweet IDs from json files located in /mnt/8TB/GITS/twitter_scraping/tweet_ids/
# Adds them to mongoDB and deletes original files
# Preface with 1st script to catch tweet IDs


import tweepy #http://www.tweepy.org/
import json
import math
import glob
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


tweet_count = db.politicians.count("id", exists= True)
print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))

import sys
import os
# Retrieve Twitter API credentials
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv"
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter05.csv" #CKT

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



def tweet_2_DB_loop(ids):
    new_additions = 0
    all_data = []
    start = 0
    end = 100
    limit = len(ids)
    i = math.ceil(limit / 100)


    for go in range(i):
        print('currently getting {} - {}'.format(start, end))
        sleep(6)  # default 6 needed to prevent hitting API rate limit
        id_batch = ids[start:end]
        start += 100
        end += 100
        tweets = api.statuses_lookup(id_batch)
        for tweet in tweets:
            #print (dict(tweet._json))
            one_id = (dict(tweet._json)['id'])
            found = collection.find({'id': one_id}).count()
            #print(one_id)
            if found == 0:
                #print(found)
                #print("inputing tweet to db")
                new_additions += 1
                pass
            #collection.find({'id': 'one_id'})
                all_data.append(dict(tweet._json))
                collection.insert(tweet._json)
            else:
                #print(found)
                #print("Tweet found in db, next")
                pass
        print ("New additions to DB : " + str(new_additions))
        print ("Political db tweet count is : " + str(tweet_count))

#tweet = json.loads(data)
#collection.insert(tweet)


tweet_ids=""
#print(glob.glob('tweet_ids/*.json'))
files = glob.glob('tweet_ids/*.json')
for x in files:
    print("Starting new list")
    with open(x, 'r') as f:
        print(x)
        ids = json.load(f)
        print('total ids: {}'.format(len(ids)))
        tweet_2_DB_loop(ids)
    print("Deleting list: " + x)
    os.remove(x)
    print("Just Deleted: " + x)
    tweet_count = db.politicians.count("id", exists= True)
    print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))

#total ids: 29772
tweet_count = db.politicians.count("id", exists= True)
print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))
