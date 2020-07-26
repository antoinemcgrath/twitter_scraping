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
db.m_quantitea.ensure_index( "id", unique=True, dropDups=True )
db.m_baratza.ensure_index( "id", unique=True, dropDups=True )
db.m_crs.ensure_index( "id", unique=True, dropDups=True )


#### Set filter watchwords
watchword_01 = ["atoms", "shoes", "feet"]
watchword_02 = ["baratza", "sette grinder", "sette coffee", "sette cafe", "sette beans"] # Contains both pdf and crs
watchword_03 = ["pdf crs"] # Contains both pdf and crs
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


count = 0


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_words = status.text
 #       print(tweet_words.encode('utf-8'))

        success_01 = False
        for word in watchword_01:
            text = word.split(" ")
            if all(one.lower() in tweet_words.lower() for one in text):
                success = True
        if success_01:
  #          print ("success!")
            print (str(watchword_01) + " is a quantitea tweet")
            db.m_quantitea.insert(status._json)

        success_02 = False
        for word in watchword_02:
            text = word.split(" ")
            if all(one.lower() in tweet_words.lower() for one in text):
                success = True
        if success_02:
#            print ("success!")
            print (str(watchword_02) + " is a quantitea tweet")
            db.m_quantitea.insert(status._json)

        success_03 = False
        for word in watchword_03:
            text = word.split(" ")
            if all(one.lower() in tweet_words.lower() for one in text):
                success = True
        if success_03:
 #           print ("success!")
            print (str(watchword_03) + " is a quantitea tweet")
            db.m_quantitea.insert(status._json)

       # print ("done this part")


    def on_error(self, status_code):
        print ("error", status_code)
        if status_code == 420:
            #returning False in on_data disconnects the stream
            print("Twitter API Rate limiting in effect, please wait")
            return False



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(api.auth,myStreamListener)
myStream.filter(track=AllWords)




#myStream.filter(track=AllWords, async=True) #Alows you to continue with terminal while it runs

#myStream.filter(track=watchword_01)
#myStream.filter(track=watchword_01, async=True)

#### Filter word or location
#napa = [-122.494125,38.201767,-122.091408,38.374501]
#napa = [-122.70,38.14,-121.90,38.49]
#napa = [-122.347441,38.276462,-122.246761,38.319639]
nyc = [-74.0,40.73,-73.0,41.73]
#myStream.filter(locations=(napa), async=True) #Persistant until connection is closed
#myStream.filter(track=['wine'], locations=(napa), async=True)
