#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

## To execute include the username as arguement
## python3 Bots_check.py AGreenDCBike

from sys import argv
script, screen_name_arg, list = argv
import botometer
import json
import tweepy
import time
import re


import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()

#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
user = Keys['Owner']


#### Bot probability
mashape_key = Twitter_Tools.get_mashape_api_keys()
twitter_app_auth = {
    'consumer_key': Keys['Consumer Key (API Key)'],
    'consumer_secret': Keys['Consumer Secret (API Secret)'],
    'access_token': Keys['Access Token'],
    'access_token_secret': Keys['Access Token Secret'],
  }



bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)

user_processing = screen_name_arg
list = list

def detect_bot(categ, one):
    try:
        result = bom.check_account(one)
        score = result['scores']['universal']
        #print(score)
        if score > 0.50:
            print(categ, ",Bot score,", score,
            #"Following:", str(one['user']['friends_count']),
            #"Followers:", str(one['user']['followers_count']),
            (",Possible bot:, www.twitter.com/" + str(result['user']['screen_name']))
            )
    except botometer.NoTimelineError as e:
        e = str(e)
        e = e.split("'screen_name': '")
        e = e[1].split("'}' has no tweets in timeline")
        e = e[0].split("', 'id_str': '")
        e = str(e[0])
        print("User has not tweeted", str("www.twitter.com/" + e))
    except tweepy.error.TweepError as e:
        got = api.get_user(one)
        got = str(got.screen_name)
        if str(e) == "Not authorized.":
            print("Private account, API not authorized", str("www.twitter.com/" + got))
        else:
            print(e)
    except Exception as e:
        got = api.get_user(one)
        got = str(got.screen_name)
        print(str("www.twitter.com/" + got), "Error", one, e)


categ = "List member"
for member in tweepy.Cursor(api.list_members, user_processing, list).items():
    detect_bot(categ,member.screen_name)


friends = api.friends_ids(user_processing)
print("Friend count:",len(friends))

followers = api.followers_ids(user_processing)
print("Followers count:",len(followers))




print("Starting: Follower count:",len(followers))
categ = "Follower"
for one in followers:
    detect_bot(categ,one)


print("Starting: Friend count:",len(friends))
categ = "Friend"
for one in friends:
    detect_bot(categ,one)
