#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

import sys
import os
import json
import csv
import time
import tweepy #http://www.tweepy.org/
from tweepy import TweepError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
connection = c = MongoClient()
db = connection.Marketing

#### Set destination database collection(s)
db.m_gdatasets.ensure_index( "id", unique=True, dropDups=True )
#db.m_baratza.ensure_index( "id", unique=True, dropDups=True )
#db.m_crs.ensure_index( "id", unique=True, dropDups=True )


#### Set filter watchwords
#watchword_01 = ["quantitea", "Tools of Titans", "ToolsofTitans"]
#watchword_02 = ["baratza", "sette grinder", "sette coffee", "sette cafe", "sette beans"] # Contains both pdf and crs
#watchword_03 = ["pdf crs"] # Contains both pdf and crs
#AllWords = watchword_01 + watchword_02 + watchword_03

#watchword_01 = ["https://t.co/L1IG83zADp"]
watchword_01 = ["https://t.co/L1IG83zADp", "https://t.co/AI3wDpfIgR", "https://t.co/Tu9EHEVvr2", "https://t.co/yC3vy4pvIa"]
watchword_02 = ["datasetsearch"] #"https://www.blog.google/products/search/making-it-easier-discover-datasets/"]
watchword_03 = ["https://toolbox.google.com/datasetsearch", "toolbox.google.com/datasetsearch"]

AllWords = watchword_01 + watchword_02 + watchword_03
print (AllWords)
print (type(AllWords))


import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
user = Keys['Owner']

print("twitter tools imported")


count = 0




#### To favorite (aka like & heart) a tweet
def favoriting_tweet(tweet):
    try:
        api.create_favorite(tweet.id_str)
        #print("Favoriting", tweet.id_str, tweet.text)
    except tweepy.TweepError as e:
        if e.api_code == 139:
            print("Your account already liked this tweet")
        else:
            print(e.api_code)
            print(e.response)
        pass
    return()

def post_link(status):
    print_tweet = status.text
    print("https://twitter.com/" + status.user.screen_name + "/status/" + str(status.id_str), print_tweet.encode('utf-8'))

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):

        tweet_words = status.text
        post_link(status)
        db.m_gdatasets.insert(status._json)
        favoriting_tweet(status)

        '''
        success_01 = False
        for word in watchword_01:
            text = word.split(" ")
            if all(one.lower() in tweet_words.lower() for one in text):
                success = True
        if success_01:
  #          print ("success!")
            print (str(watchword_01) + " is a toolbox search")
            db.m_gdatasets.insert(status._json)

        success_02 = False
        for word in watchword_02:
            text = word.split(" ")
            if all(one.lower() in tweet_words.lower() for one in text):
                success = True
        if success_02:
#            print ("success!")
            print (str(watchword_02) + " is a toolbox link")
            db.m_gdatasets.insert(status._json)

        success_03 = False
        for word in watchword_03:
            text = word.split(" ")
            if all(one.lower() in tweet_words.lower() for one in text):
                success = True
        if success_03:
#            print ("success!")
            print (str(watchword_03) + " is a base toolbox link with no https")
            db.m_gdatasets.insert(status._json)

        def on_error(self, status_code):
             print ("error", status_code)
             if status_code == 420:
                 #returning False in on_data disconnects the stream
                 print("Twitter API Rate limiting in effect, please wait")
                 return False


        tweet_links = str(status.entities)

        success_01 = False
        for word in watchword_01:
            text = word.split(" ")
            if all(one.lower() in tweet_links.lower() for one in text):
                success = True
        if success_01:
        #          print ("success!")
            print (str(watchword_01) + " is a toolbox search")
            db.m_gdatasets.insert(status._json)

        success_02 = False
        for word in watchword_02:
            text = word.split(" ")
            if all(one.lower() in tweet_links.lower() for one in text):
                success = True
        if success_02:
        #            print ("success!")
            print (str(watchword_02) + " is a toolbox link")
            db.m_gdatasets.insert(status._json)

        success_03 = False
        for word in watchword_03:
            text = word.split(" ")
            if all(one.lower() in tweet_links.lower() for one in text):
                success = True
        if success_03:
        #            print ("success!")
            print (str(watchword_03) + " is a base toolbox link with no https")
            db.m_gdatasets.insert(status._json)
        '''

        def on_error(self, status_code):
             print ("error", status_code)
             if status_code == 420:
                 #returning False in on_data disconnects the stream
                 print("Twitter API Rate limiting in effect, please wait")
                 return False


print("Stream Listener defined")
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(api.auth,myStreamListener)
myStream.filter(track=AllWords)



