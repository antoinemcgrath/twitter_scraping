#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

#### One day you wake up to find that hundreds of Twitter users unfollowed you.
####      Was it something I said?
#### Perhaps not. Perhaps they were bots and have all been banned.
#### Whatever the reason this script can help you get to the bottom of it.
####
#### Run this code at will to create periodic .txt records of users following you on Twitter.

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
list_owner = Keys['Owner']

#### Get list of followers IDs
followers = api.followers_name('16028499')
print("Follower count:",len(followers))

epoch_time = int(time.time())
path = "backups/"+str(epoch_time)+str("__UsersFollowingPrima.txt")

for a_user_id in followers:
    with open(path,"a+") as file:
        file.write(str(a_user_id.screen_name) + ",    " + str(a_user_id.description) + '\n')
    Twitter_Tools.twitter_rates(api)
    sleep(20)

