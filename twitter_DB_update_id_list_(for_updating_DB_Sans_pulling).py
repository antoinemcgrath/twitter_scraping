#!/usr/bin/python


###########Lines 195 for example reset DB values inorder to overwrite crawled dates and recrawl (due to unnotticed downtime)

import random
import sys
import os
import json
import math
import glob
import csv
import time
import datetime
from datetime import datetime as dt
tday = datetime.date.today()
today = str(tday)

#print (tday)
from datetime import date
#from datetime import datetime
from time import sleep
import tweepy #http://www.tweepy.org/
from tweepy import TweepError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
connection = c = MongoClient() #connection = c = MongoClient(localhost', '27017') #connection = Connection('localhost', '27017')
extradelay = 1
days_per_query = 20
from os.path import exists

####

#### Add users to DB from specified twitter group list
# For: https://twitter.com/AGreenDCBike/lists/climatepolitics-info
# Run: python3 twitter_DB_update_id_list.py AGreenDCBike climatepolitics-info
list_host = str(sys.argv[1:2])[2:-2] #Example: 'AGreenDCBike'
list_name = str(sys.argv[2:3])[2:-2]#Example: 'climatepolitics-info'


#list_host = 'AGreenDCBike'
#list_name = 'climatepolitics-info'

#'Pete_Weldy' 'california-dems'
#'ericlinder' 'ca-assembly-members'
#'apen4ej' 'california-state-senate'
#'apiahf' 'ca-state-assembly'
#'cspan' 'members-of-congress'
#'cspan' 'foreign-leaders'
#'cspan' 'governors'
#'cspan' 'u-s-representatives'
#'cspan' 'senators'
#'AGreenDCBike' 'us-gov'
#'AGreenDCBike' 'climatepolitics-info'

#### Set which twitter API credentials to access

#Setup Twitter
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv" #
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter02.csv" #AGreenDCBike
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter03.csv" #
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter05.csv" #

list_dir = "tweet_ids_list/"
if not os.path.exists(list_dir):
    os.makedirs(list_dir)




def connect_mongoDB():
    #print("Loop2")
    db = connection.Twitter #db.tweets.ensure_index("id", unique=True, dropDups=True)
    print("Mongo Twitter DB Connected")
    # The MongoDB connection info. Database name is Twitter and your collection name is politicians.
    db.politicians.ensure_index( "id", unique=True, dropDups=True )
    collection = db.politicians
    print("Collection politicians connected")
    # The MongoDB connection info. Database name is Twitter and your collection name is id_politicians.
    db.id_politicians.ensure_index( "id", unique=True, dropDups=True )
    id_collection = db.id_politicians
    print("Collection id_politicians connected")
    #### tweet_count = db.politicians.count("id", exists= True)
    #### print ("Total tweet count in DB is: " + str(tweet_count))
    #return(db, collection, id_collection)
    return(collection, id_collection)



database_connections = connect_mongoDB()
#db = database_connections[0]
collection = database_connections[0]
id_collection = database_connections[1]

# Retrieve Twitter API credentials
import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth)
user = Keys['Owner']


#### 2DO (Add pull from twitter API of list)
#### Retrieve a list of users from twitter lists and add them to the DB if they do not exists
def get_twit_list():
    #print("Loop4")
    twit_list = []
    twitter_pull = tweepy.Cursor(api.list_members, list_host, list_name).items()
    for user in twitter_pull:
        twit_list.append(user.screen_name)
    ####twit_list =  ['realDonaldTrump', 'BarackObama'] #Example list
    return (twit_list)



################
######## This definition should be improved (after the rest gets improved)
#### Add new users from twit list to the DB (id collection)
def add_new_twit_list_members_to_db():
    #print("Loop5")
    all_data = []
    start = 0
    end = 100
    limit = len(twit_list)# print (limit)
    i = math.ceil(limit / 100)   # print (i)
    for go in range(i):
        print('Looking up users {} - {}'.format(start, end))
        sleep(12)  # default 6 needed to prevent hitting API rate limit
        id_batch = twit_list[start:end]
        start += 100
        end += 100
        #tweets = api.statuses_lookup(id_batch)
        u_lists = api.lookup_users(screen_names = id_batch)
        for one_of_many in u_lists:
            all_data.append(dict(one_of_many._json))
    user_add_count = 0
    user_json = all_data
    for a_user in user_json:
        one_id = ((a_user)['id'])   #print(one_id)
        found = id_collection.find({'id': one_id}).count()
        name = str((a_user)['screen_name'])
        if found == 0:        #### New user add to DB
            print("Uploading new user " + name + " to db")
            user_add_count = user_add_count + 1
            id_collection.insert(a_user)
            Account_Start = (a_user)['created_at']
            _accountStart = _grabStart = _grabEnd = time.strftime('%Y-%-m-%-d', time.strptime(Account_Start,'%a %b %d %H:%M:%S +0000 %Y'))
            _db_itemcreated = _db_itemupdated = datetime.datetime.now()#collection.find({'id': one_id})        #= (a_user._json)['created_at']
            id_collection.update({'id': one_id},{'$set' : {"_accountStart":_accountStart}})
            id_collection.update({'id': one_id},{'$set' : {"_grabStart":_accountStart}})
            id_collection.update({'id': one_id},{'$set' : {"_grabEnd":_accountStart}})


            pass
        else:
            print("not found")
            pass
    print (str(user_add_count) + " new users were added to the DB")
#############
#############
#input("Press Enter to add new users to DB ")

























####
###input("Press Enter to retrieve users names from twitter list")
try:
    sys.argv[2]
    #print(sys.argv[2:3])
    #print(sys.argv[2:3])
except IndexError:
    sys_arg_exists = False
    print("No new list provided for addition to DB")
else:
    sys_arg_exists = True
    twit_list = get_twit_list()
    print ("if list host error follows the problem is that sysarg[2:3] exists as blank")
    print (list_host)
    print (list_name)
    print (str(twit_list))
    print (len(twit_list))
    print("Adding list of handles to DB")
    add_new_twit_list_members_to_db()









#### Searc mongo return users who's dates are not today (tday)



#### Get DB list to update
def get_user_list():
    #print("Loop6")
    print("getting db user list to update")
    user_list = []
    #for x in id_collection.find({"_grabEnd": {'$ne': "2009-03-30" }},{"screen_name": 1}):
    for x in id_collection.find():#.sort({"_grabStart": -1}):
        diction = x
        user_list.append(diction['screen_name'])
    #print (user_list)
    print ("User list length is: " + str(len(user_list)))
    print ("User list length is: " + str(len(user_list)))
    print ("User list length is: " + str(len(user_list)))
    print ("User list length is: " + str(len(user_list)))

    return (user_list)

user_list = get_user_list()
#ser_json = api.lookup_users(screen_names = user_list)

















all_data = []
start = 0
end = 100
limit = len(user_list)
#print (limit)
i = math.ceil(limit / 100)
#print (i)
user_list = list(reversed(user_list))

for go in range(i):
    print('Looking up users {} - {}'.format(start, end))
    sleep(1)  # needed to prevent hitting API rate limit
    id_batch = user_list[start:end]
    start += 100
    end += 100
    #tweets = api.statuses_lookup(id_batch)
    #print(id_batch)
    u_lists = api.lookup_users(screen_names = id_batch)
    print(len(u_lists))
    for one_of_many in u_lists:
        #print("PRINTING ONE OF MANY")
        #print(one_of_many)
        try:
            all_data.append(dict(one_of_many._json))
        except tweepy.error.TweepError as e:
            print ("Tweepy Error")
            print (e)
            print("PRINTING ONE OF MANY")
            print(one_of_many)





def generate_url(name, _grabStart, _grabEnd):
    print("F1 Generate URL Loop")
    url_A = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    url_B =  name + '%20since%3A' + str(_grabStart) + '%20until%3A' + str(_grabEnd) + 'include%3Aretweets&src=typd'
    url = url_A + url_B
    return (url)

def fetch_tweets(url):
    print("F2 Fetch Tweets Loop")
    #print(str(url))
    ids = []

    #### Detect Blocking

    try:   ##### Write twitter IDs to ID list json files
        print("try writing1")
        with open(list_dir + twitter_ids_filename) as f:
            all_ids = ids + json.load(f)
            data_to_write = list(set(all_ids))
    except FileNotFoundError:
        print("try writing2")
        with open(list_dir + twitter_ids_filename, 'w') as f:
            all_ids = ids
            data_to_write = list(set(all_ids))
    with open(list_dir + twitter_ids_filename, 'w') as outfile:
        json.dump(data_to_write, outfile)
        print("try writing3")


def update_progress(_grabStart, _grabEnd, fetch_count, fetch_sessions, _accountStart):
    print("F3 Update DB Loop")
    if str(_grabEnd) < str(tday):
        print("Writing _grabEnd as new start into DB start")
        print(str(_grabEnd))
        print(str(tday))
        #id_collection.update({'id': one_id},{'$set' : {"_grabStart":str(_grabEnd)}}) ##Updates id_DB to reflect latest crawl
        id_collection.update({'id': one_id},{'$set' : {"_accountStart":_accountStart}})
        id_collection.update({'id': one_id},{'$set' : {"_grabStart":_accountStart}})
        id_collection.update({'id': one_id},{'$set' : {"_grabEnd":_accountStart}})
    else:
        print("Writing tday into DB start")
        print(str(_grabEnd))
        print(str(tday))
        #id_collection.update({'id': one_id},{'$set' : {"_grabStart":str(tday)}}) ##Updates id_DB to reflect latest crawl
        id_collection.update({'id': one_id},{'$set' : {"_accountStart":_accountStart}})
        id_collection.update({'id': one_id},{'$set' : {"_grabStart":_accountStart}})
        id_collection.update({'id': one_id},{'$set' : {"_grabEnd":_accountStart}})



    fetch_count += 1
    print (str(fetch_sessions) + " fetches needed " + str(fetch_count) + " completed")
    return(fetch_count)

def initiate_pull(name, _grabStart, _grabEnd, fetch_count, fetch_sessions, _accountStart):
    print("F0 Initiating Pull Loop")
    url = generate_url(name, _grabStart, _grabEnd)
    fetch_tweets(url)
    fetch_count = update_progress(_grabStart, _grabEnd, fetch_count, fetch_sessions, _accountStart)
    return(fetch_count)


############Update to fetch specific user based on oldest _starDate
#### Retrieve data from DB on existing user
for another_user in all_data:
    print(len(all_data))
    start_timer = time.time()
    name = str(dict(another_user)['screen_name'])
    one_id = (dict(another_user)['id'])   #print(one_id)
    working_id = id_collection.find({'id': one_id})
    found = working_id.count()


    if found != 1:    #### If user is not in DB once then present an error
        print ("Error with user twitter id: " +str(one_id))
        if found == 0:
            print("Error note: ID not in DB despite earlier attempt to add it, we may be failing to add the account because it was earlier deleted from twitter")
        else:
            print ("Error note: ID in the DB more than once")  #input("Press Enter to continue")
    else:    #### Existing user access found once, fetch their last tweet capture dates
        print("we have a user to work on, line 490") #
        for x in working_id:  #for x in id_collection.find(({'id': one_id})):

            diction = x
            twitter_ids_filename = 'tweet_ids_' + name+'.json'
            name = diction['screen_name']
            _accountStart = diction['_accountStart']
            _grabStart = diction['_grabStart']
            _grabEnd = diction['_grabEnd']
            days = 1
            fetch_days = str(days)
            fetch_sessions = math.ceil(float(int(fetch_days)/days_per_query))
            fetch_count = 0



            while fetch_count <= fetch_sessions:
                #print("while loop triggered")
                fetch_count = initiate_pull(name, _grabStart, _grabEnd, fetch_count, fetch_sessions, _accountStart)
                ####Incrament the values searched
                ##_grabStart += datetime.timedelta(days=days_per_query)
                ##_grabEnd = _grabStart + datetime.timedelta(days=days_per_query)
                #print(str(fetch_count))
                #print("Escaped from while loop")
                end_timer = time.time()
                total_t = end_timer - start_timer
                #print(str("%.0f" % ((total_t)/60)) + " minutes taken. to add " + fetched_days + " days. " + str(len(data_to_write)) + " tweets in the file of " + str(name) )
                print(str("%.0f" % ((total_t)/60)) + " minutes taken to update the file of " + str(name) )






                ####tday-_grabStart

                #_grabStart = dt.date(dt.strptime(diction['_grabStart'], '%Y-%m-%d'))
                #_grabEnd = dt.date(dt.strptime(diction['_grabEnd'], '%Y-%m-%d'))
                #days_to_fetch = int(str(tday-_grabStart).split(" ")[0])
                #print("Fetching : " + days_to_fetch + " days.
                #print("Starting with: " + str(_grabStart))
                #print("Through: " + today)
