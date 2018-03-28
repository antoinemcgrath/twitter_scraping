#!/usr/bin/python3

## To execute include the username as arguement
## python3 Bots_check.py AGreenDCBike

from sys import argv
script, screen_name_arg = argv
import botometer
import json
import tweepy
import time
import re


import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()

user = Keys['Owner']


#### Bot probability
mashape_key = keys_json["mashape_key"]
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


friends = api.friends_ids(user_processing)
print("Friend count:",len(friends))

followers = api.followers_ids(user_processing)
print("Follower count:",len(followers))


def detect_bot(one):
    try:
        result = bom.check_account(one)
        score = result['scores']['universal']
        #print(score)
        if score > 0.50:
            print("Bot score:", score, "Possible bot: www.twitter.com/" + str(result['user']['screen_name']))
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


print("Starting: Follower count:",len(followers))
for one in followers:
    detect_bot(one)

print("Starting: Friend count:",len(friends))
for one in friends:
    detect_bot(one)
