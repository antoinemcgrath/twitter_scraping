#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

#### A script for exporting twitter data of a specific list

#### Specify your list
list = 'members-of-congress'
user = 'cspan' # Or allow to be set as the key owner user on line ~#22
backups_dir = "backups"

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
collection = db.politicians
import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
user = Keys['Owner']


#### Get list of user ids from those within the list of interest
listed = []
for page in tweepy.Cursor(api.list_members, user, list).pages():
    listed.extend(page)
    time.sleep(6)
    Twitter_Tools.twitter_rates(api)
    print(len(listed))


list2=[]
for one in listed:
    list2.append(one.screen_name)


def get(name):
    cursor = db.politicians.find({"user.screen_name": name, "retweeted": False })
    cursor.count()
    return dumps(cursor)



#### Create directories when they do not exist
def make_path_exist( path):
    try:
        os.makedirs( path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

make_path_exist(backups_dir)

backups_list_dir = backups_dir + "/" + list
make_path_exist(backups_list_dir)

for name in list2:
    cat = get(name)
    text_file = open( backups_list_dir + "/" + name + ".json", "w")
    text_file.write(cat)
    text_file.close()
