#!/usr/bin/python


#######################################################################################################################
#### A big thank you to https://github.com/bpb27 for the base/seed code https://github.com/bpb27/twitter_scraping  ####
#######################################################################################################################
#### MongoDB enhanced version at: https://github.com/antoinemcgrath/twitter_scraping


#### twitter_DB_update_id_list.py
#### --Collect tweet ids & update mongo DB with collection progress
##
#### twitter_DB_update_tweets_metadata.py
#### --Query API with tweet ids & add json response to mongoDB
##
#### cron__twitter_DB_update_id_list.py
#### --Check first to see if the code is running before starting it (for cron starts)
##
#### This two step disjunction allows one to add tweets to your DB from a list of tweet ids that others have collected
#### Likewise this method allows one to share lists of tweetids


# cd /mnt/8TB/GITS/twitter_scraping
# python3 twitter_DB_update_tweets_metadata.py

# Retrieves tweet IDs from json files located in /mnt/8TB/GITS/twitter_scraping/tweet_ids/
# Adds them to mongoDB and deletes original files



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


path = 'tweet_ids_list/'

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

import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth)
user = Keys['Owner']


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
        #print ("New additions to DB : " + str(new_additions))
        #print ("Political db tweet count is : " + str(tweet_count))

#tweet = json.loads(data)
#collection.insert(tweet)


tweet_ids=""
#print(glob.glob(path +'*.json'))

#files = glob.glob(path+'*.json')
files_big2small = files_small2big = []
files_small2big = sorted(glob.glob(path+'*.json'), key=os.path.getmtime)
#files_small2big = sorted(glob.glob(path+'*.json'), key=os.path.getsize)
for fi in reversed(files_small2big):
    files_big2small.append(fi)

files = files_big2small


for x in files:
    #print("Starting new list")
    try:
        with open(x, 'r') as f:
            #print(x)
            ids = json.load(f)
            print( x + (' total tweet ids: {}'.format(len(ids))))
            tweet_2_DB_loop(ids)
            with open(x, 'w') as f:
               f.write("[]")
        #print("Emptied list: " + x)
        #os.remove(x)

        tweet_count = db.politicians.count("id", exists= True)
        print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))


    except tweepy.error.TweepError:
        print ("tweepy error")
        with open(twitterKEYfile2, 'r') as f:
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
        try:
           with open(x, 'r') as f:
               #print(x)
               ids = json.load(f)
               print( x + (' total tweet ids: {}'.format(len(ids))))
               tweet_2_DB_loop(ids)
           #print("Deleting list: " + x)
           #os.remove(x)
           #print("Just Deleted: " + x)
           tweet_count = db.politicians.count("id", exists= True)
           print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))
        except tweepy.error.TweepError:
           print ("tweepy error")

        #if e.response.status_code == 404:
        #    print ("%s does not exist" % (twitter_id))
            #return None
#total ids: 29772
tweet_count = db.politicians.count("id", exists= True)
print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))



##### UPDATE DATES TO UNIX

import json
import math
from pymongo import MongoClient
import datetime
connection = c = MongoClient()
db = connection.Twitter
#db.tweets.create_index("id", unique=True, dropDups=True)
db.politicians_test.ensure_index( "id", unique=True, dropDups=True )
collection = db.politicians_test


##Similar direct in mongo## db.politicians_test.find().forEach(function(doc){doc.created_at = new Date(doc.created_at);db.politicians_test.save(doc)})
from bson.objectid import ObjectId
not_UNIXtimed = db.politicians.find({ "created_at": {'$exists': True}, "user.created_at": {'$exists': True}, "created_at_UNIXtime": {'$exists': False}})
not_UNIXtimed.count()
for one_item in not_UNIXtimed:
    one_created_at_UNIXtime = (int(datetime.datetime.strptime(one_item['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%s")))
    one_usercreated_at_UNIXtime = (int(datetime.datetime.strptime(one_item['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%s")))
    one_id = (str(one_item['_id']))
    print (one_id +" "+ str(one_created_at_UNIXtime) +" "+ str(one_usercreated_at_UNIXtime))
    db.politicians.update_one({'_id': ObjectId(one_id)}, {'$set': {'created_at_UNIXtime': one_created_at_UNIXtime, 'user.created_at_UNIXtime': one_usercreated_at_UNIXtime}})
