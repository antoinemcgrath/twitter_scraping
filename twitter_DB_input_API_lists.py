#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################


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

db = connection.Twitter
db.politicians.ensure_index( "id", unique=True, dropDups=True )
collection = db.politicians

tweet_count = db.politicians.count("id", exists= True)
print ("DB:Twitter Collection:political tweets count is : " + str(tweet_count))

import sys
import os



import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
user = Keys['Owner']



twitter_user = "AGreenDCBike"
tw_lists = ["candidates", "us-ca-assembly", "us-ca-bill"]

for tw_list in tw_lists:
    count = 0
    new_additions = 0
    try:
        #API.list_timeline(owner, slug[, since_id][, max_id][, per_page][, page])
        twrecents = api.list_timeline(owner_screen_name=twitter_user, slug=tw_list, count=300)
        # http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html?highlight=lists
        #
        #  for a_tweet in tweepy.Cursor(api.list_timeline(owner_screen_name=twitter_user, slug=tw_list, count=200)).items(200):
        # Would this enable me to go further back in timeline?: General Stream Search # for tweet in tweepy.Cursor(api.search, q="google", rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(200):
        # The new method is more efficient http://docs.tweepy.org/en/v3.5.0/cursor_tutorial.html?highlight=lists
        for tweet in twrecents:
            all_data = []
            count = count + 1
            #print (count, tweet.id_str, tweet.created_at, tweet.text) #print (dict(tweet._json))
            one_id = (dict(tweet._json)['id'])
            found = collection.find({'id': one_id}).count()
            if found == 0:
                #print("inputing tweet to db")
                new_additions += 1

                #### Date calculations
                #print(dict(tweet._json)['created_at'])
                one_created_at_UNIXtime = (int(datetime.datetime.strptime(dict(tweet._json)['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%s")))
                one_usercreated_at_UNIXtime = (int(datetime.datetime.strptime(dict(tweet._json)['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%s")))
                #print(one_usercreated_at_UNIXtime)
                data = dict(tweet._json)
                ## Merge embedded dictionaries {user}
                json_user_addition = {'created_at_UNIXtime': one_usercreated_at_UNIXtime}
                json_addition = {'created_at_UNIXtime': one_created_at_UNIXtime}
                #new_json_user = {**(data['user']), **(json_user_addition)}
                data['user'].update(json_user_addition)
                data.update(json_addition)
                #print (data)
                all_data.append(data)
                collection.insert(data)
                pass
            else:
                #print(found)
                #print("Tweet found in db, next")
                pass

        print(str(tw_list) + " has new tweets: " + str(new_additions))

        #print ("New additions to DB : " + str(new_additions))
        #api.get_list(slug=tw_list_id, owner_screen_name=twitter_user)
    except tweepy.error.TweepError as e:
        print ("Tweepy Error")
        print (e)

        #tweets = api.statuses_lookup(id_batch)
        #twitter_pull = tweepy.Cursor(api.list_members, list_host, list_name).items()
