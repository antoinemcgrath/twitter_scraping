#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

#### A script for archiving the api user's likes with Twitter DB collection "liked"


import os
import json
import tweepy
import re
import time
import errno
from bson.json_util import dumps
from pymongo import MongoClient
connection = c = MongoClient()

db = connection.Twitter
collection = db.liked
import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = Keys['Owner']
print(user)
time.sleep(5)
likes_archived = 0
likes_unliked = 0
UserOI = user #Can be another user (sans unlike ability)


def unlike_likes(likes_archived,likes_unliked):
    favs_count = api.get_user(UserOI).favourites_count
    print("User's favorites:", favs_count)
    for favorite in tweepy.Cursor(api.favorites, id=UserOI).items(favs_count):
        print("Got favorites")
        print("Id string:", favorite.id_str)
        try:
            found = collection.find({'id_str': favorite.id_str}).count() #searching db
            if found == 0:
                collection.insert(favorite._json)
                likes_archived += 1
            api.destroy_favorite(favorite.id)
            likes_unliked += 1
            p_text = ("Likes unliked: " + str(likes_unliked) + " Likes archived: " + str(likes_archived))
            print(p_text)
        except Exception as e:
            print(e)
            if 144 is e:
                sleep(11)
            else:
                input("Tenacious error, press enter to skip user...")


unlike_likes(likes_archived,likes_unliked)
