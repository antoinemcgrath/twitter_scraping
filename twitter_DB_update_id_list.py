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
##
##
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
#
#
# cd /mnt/8TB/GITS/twitter_scraping
# python3 twitter_DB_update_id_list.py
#
# Compiles all tweet ids fetched from a users single day timeline & updates mongodb with the date completed
# Example of gnerated URL: https://twitter.com/search?f=tweets&vertical=default&q=from%3ABarackObama%20since%3A2016-03-14%20until%3A2016-03-15include%3Aretweets&src=typd
#######################################################################################################################


import re
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
driver = None
from datetime import date
from time import sleep
import tweepy #http://www.tweepy.org/
from tweepy import TweepError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
connection = c = MongoClient()
#connection = c = MongoClient('localhost', '27017') #connection = Connection('localhost', '27017')
delay = 1 + 1000/(random.getrandbits(12))
extradelay = 12.2
days_per_query = 30
from os.path import exists
#### Arrising Errors
#selenium.common.exceptions.TimeoutException: Message: timeout: cannot determine loading status
import urllib
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.command import Command

import logging
#logging.basicConfig(filename='python_debug.log',level=logging.DEBUG) #Stores all runs
logging.basicConfig(filename='python_debug.log', filemode='w', level=logging.DEBUG) #Stores last run
#logging.debug('')#logging.info('')#logging.warning('')

#### Add users to DB from specified twitter group list
# For: https://twitter.com/AGreenDCBike/lists/climatepolitics-info
# Run: python3 twitter_DB_update_id_list.py AGreenDCBike climatepolitics-leaders
list_host = str(sys.argv[1:2])[2:-2] #Example: 'AGreenDCBike'
list_name = str(sys.argv[2:3])[2:-2]#Example: 'climatepolitics-info'

#list_host = 'AGreenDCBike'
#list_name = 'climatepolitics-leaders'

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
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv"
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv" #ck

import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth)
user = Keys['Owner']


list_dir = "tweet_ids_list/"
if not os.path.exists(list_dir):
    os.makedirs(list_dir)

####Close existing webdriver activity
import psutil
PROCNAME = "chromedriver"
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()



def connect_mongoDB():
    db = connection.Twitter #db.tweets.ensure_index("id", unique=True, dropDups=True)
    print("Mongo Twitter DB Connected")
    # The MongoDB connection info. Database name is Twitter and your collection name is politicians.
    db.politicians.ensure_index( "id_str", unique=True, dropDups=True )
    collection = db.politicians
    print("Collection politicians connected")
    # The MongoDB connection info. Database name is Twitter and your collection name is id_politicians.
    db.id_politicians.ensure_index( "id_str", unique=True, dropDups=True )
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


#### 2DO (Add pull from twitter API of list)
#### Retrieve a list of users from twitter lists and add them to the DB if they do not exists
def get_twit_list():
    logging.debug("Loop4")
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
    logging.debug("Loop5")
    all_data = []
    start = 0
    end = 100
    limit = len(twit_list)# print (limit)
    i = math.ceil(limit / 100)   # print (i)
    for go in range(i):
        print('Looking up users {} - {}'.format(start, end))
        sleep(delay)  # default 6 needed to prevent hitting API rate limit
        id_batch = twit_list[start:end]
        start += 100
        end += 100
        #tweets = api.statuses_lookup(id_batch)
        u_lists = api.lookup_users(screen_names = id_batch)
        for one_of_many in u_lists:
            #print(one_of_many)
            all_data.append(dict(one_of_many._json))
    user_add_count = 0
    user_json = all_data
    logging.debug(user_json)
    logging.debug(id)
    for a_user in user_json:
        one_id = str((a_user)['id']) #twitter data
        logging.debug(one_id)
        logging.debug((a_user)['id'])
        found = id_collection.find({'id_str': one_id}).count() #searching db
        name = str((a_user)['screen_name'])
        if found == 0:        #### New user add to DB
            print("Uploading new user " + name + " to db")
            user_add_count = user_add_count + 1
            id_collection.insert(a_user)
            Account_Start = (a_user)['created_at']
            _accountStart = _grabStart = _grabEnd = time.strftime('%Y-%-m-%-d', time.strptime(Account_Start,'%a %b %d %H:%M:%S +0000 %Y'))
            _db_itemcreated = _db_itemupdated = datetime.datetime.now()#collection.find({'id_str': one_id})        #= (a_user._json)['created_at']
            id_collection.update({'id_str': one_id},{'$set' : {"_accountStart":_accountStart}}) #FAILURE Did not ASSIGN DB VALUE TYPE AS 9 (DATE) id_collection.update({'id_str': one_id},{'$set' : {"_accountStart": {$field:9  int(_accountStart)}  }}) ##https://docs.mongodb.com/manual/reference/operator/query/type/
            id_collection.update({'id_str': one_id},{'$set' : {"_grabStart":_grabStart}})
            #id_collection.update({'id_str': one_id},{'$set' : {"_grabEnd":_grabStart}})#collection.find({"$text": {"$search": str("realDonaldTrump"), '$caseSensitive': False}}).count()        #collection.find({ '$text': { '$search': 'realDonaldTrump', '$caseSensitive': True } }).count()
            ###for x in id_collection.find(({'id_str': one_id})):
            ###    diction = x
            ###    _grabStart = dt.date(dt.strptime(diction['_grabStart'], '%Y, %m, %d'))
            ###    _grabEnd = dt.date(dt.strptime(diction['_grabEnd'], '%Y, %m, %d'))
            pass
        else:
            pass
    print (str(user_add_count) + " new users were added to the DB")
#############
#############
#input("Press Enter to add new users to DB ")




####
###input("Press Enter to retrieve users names from twitter list")
try:
    sys.argv[2]
    logging.debug(sys.argv[2:3])
    logging.debug(sys.argv[2:3])
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



#### Search mongo return users who's dates are not today (tday)



#### Get DB list to update
def get_user_list():
    logging.debug("Loop6")
    print("getting db user list to update")
    user_list = []
    #for x in id_collection.find({"_grabEnd": {'$ne': "2009-03-30" }},{"screen_name": 1}):
    for x in id_collection.find({"_grabEnd": {'$ne': today}},{"screen_name": 1}):#.sort({"_grabStart": -1}):
        diction = x
        user_list.append(diction['screen_name'])
    #print (user_list)
    ###### LIST SHORTCUT
    ######user_list = ['Steve_Glazer','AsmFrazier','KansenChu','CBakerAD16','Baker4Assembly']
    print ("User list length is: " + str(len(user_list)))
    return (user_list)
####driver.quit()
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
    sleep(delay)  # needed to prevent hitting API rate limit
    id_batch = user_list[start:end]
    start += 100
    end += 100
    #tweets = api.statuses_lookup(id_batch)
    #print(id_batch)
    u_lists = api.lookup_users(screen_names = id_batch)
    print(len(u_lists))
    for one_of_many in u_lists:
        logging.debug("PRINTING ONE OF MANY")
        logging.debug(one_of_many)
        try:
            all_data.append(dict(one_of_many._json))
        except tweepy.error.TweepError as e:
            print ("Tweepy Error")
            print (e)
            print("PRINTING ONE OF MANY")
            print(one_of_many)




def generate_url(name, _grabStart, _grabEnd):
    logging.debug("F1 Generate URL Loop")
    url_A = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    url_B =  name + '%20since%3A' + str(_grabStart) + '%20until%3A' + str(_grabEnd) + 'include%3Aretweets&src=typd'
    url = url_A + url_B
    return (url)

def fetch_tweets(url, driver, tweet_selector, id_selector):
    logging.debug("F2 Fetch Tweets Loop")
    #print(str(url))
    ids = []

    #### Detect Blocking
    number_of_attempts = 0
    #print(number_of_attempts)
    #print("while")
    while number_of_attempts < 5:
       number_of_attempts += 1
       #print("try")
       try:
          #print("try start")
          driver.get(url)
          #print("try done")

       except TimeoutException as ex:
           print("except error start")
           print(ex.Message)
           driver.navigate().refresh()
           print("except error done")
       page_source = driver.page_source

       if re.search(r"20.. Twitter", page_source):
           break
       else:
           print("Twitter site not accessed")
           sleep(300)
    else:
        input("Press Enter to continue")


    logging.debug("if")
    if page_source.find(".block") > 0:
        mydate = datetime.datetime.now()
        print(page_source)
        print (mydate.strftime('Blocked at is %d %B'))
        extradelay = extradelay + extradelay + 1000/(random.getrandbits(12))
        print("Sleeping for " + str(extradelay))
        sleep(extradelay)

    else:
        #print ("Delaying")
        delay = (extradelay + 1000/(random.getrandbits(12)))

        sleep(delay+extradelay)
        #print("scraping0 updating +10 dbbbbbbbbbb     " + (str(d2)))
        #id_collection.update({'id_str': one_id},{'$set' : {"_grabStart":d2}})
        #id_collection.update({'id_str': one_id},{'$set' : {"_grabEnd":d2}})

        #### Scroll through page load page grab tweet IDs
        try:
            #print("trying to found tweets")
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            #print("scraping1")
            increment = 10
            while len(found_tweets) >= increment:
                #print('Loading page to load more tweets')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(delay)
                found_tweets = driver.find_elements_by_css_selector(tweet_selector)
                increment += 10
            print('{} tweets fetched'.format(len(found_tweets)))
            for tweet in found_tweets:
                #print("Escaping scraping 1 loop")
                try:
                    #print("good")
                    id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                    #print("great")
                    ids.append(id)
                    #print("appended")
                except StaleElementReferenceException as e:
                    print('lost element reference', tweet)
            #print("scraping2")
        except NoSuchElementException:
            pass
            #print('no tweets on this day')
        try:   ##### Write twitter IDs to ID list json files
            #print("Open file if exists")
            with open(list_dir + twitter_ids_filename) as f:
                all_ids = ids + json.load(f)
                data_to_write = list(set(all_ids))
        except FileNotFoundError:
            #print("FILE DOES NOT EXIST, creating file")
            all_ids = ids
            data_to_write = list(set(all_ids))
        #print("writting to file")
        with open(list_dir + twitter_ids_filename, 'w') as outfile:
            json.dump(data_to_write, outfile)
            #print("Wrote to file")


def update_progress(_grabStart, _grabEnd, fetch_count, fetch_sessions, one_id):
    #print("F3 Update DB Loop")
    if str(_grabEnd) < str(tday):
        #print("Writing _grabEnd as new start into DB start")
        #print(str(one_id))
        #print(str(id_collection))
        #print(str(_grabStart))
        #print(str(_grabEnd))
        #print(str(tday))
        id_collection.update({'id_str': one_id},{'$set' : {"_grabStart":str(_grabEnd)}}) ##Updates id_DB to reflect latest crawl
        id_collection.update({'id_str': one_id},{'$set' : {"_grabEnd":str(_grabEnd)}}) ##Updates id_DB to reflect latest crawl
        #print("Updated end and start")
    else:
        #print("Writing tday into DB start")
        #print(str(_grabEnd))
        #print(str(tday))
        id_collection.update({'id_str': one_id},{'$set' : {"_grabStart":str(tday)}}) ##Updates id_DB to reflect latest crawl
        id_collection.update({'id_str': one_id},{'$set' : {"_grabEnd":str(tday)}}) ##Updates id_DB to reflect latest crawl
    fetch_count += 1
    #print (str(fetch_sessions) + " fetches needed " + str(fetch_count) + " completed")
    return(fetch_count)

def initiate_pull(name, _grabStart, _grabEnd, fetch_count, fetch_sessions, one_id, driver, tweet_selector, id_selector):
    #print("F0 Initiating Pull Loop")
    url = generate_url(name, _grabStart, _grabEnd)
    fetch_tweets(url, driver, tweet_selector, id_selector)
    fetch_count = update_progress(_grabStart, _grabEnd, fetch_count, fetch_sessions, one_id)
    return(fetch_count)









def action_loop():
    _grabStart = dt.date(dt.strptime(diction['_grabStart'], '%Y-%m-%d'))
    _grabEnd = _grabStart + datetime.timedelta(days=days_per_query)
    days = (tday - _grabStart).days + 1
    fetch_days = str(days)
    fetch_sessions = math.ceil(float(int(fetch_days)/days_per_query))
    fetch_count = 0
    #print( name + " Days to fetch: " + str(fetch_days) + " Fetch sessions required: " + str(fetch_sessions) + " Current fetch count: " + str(fetch_count))
    #print ("Fetched span: " + str(_grabStart) + " " + str(_grabEnd))
    chrome_options = Options() ##Note woah selenium extensions enabling https://stackoverflow.com/questions/16511384/using-extensions-with-selenium-python
    chrome_options.add_argument('--dns-prefetch-disable') ##options are Safari() Chrome() Firefox() Safari()
    driver = Chrome(chrome_options=chrome_options) ##driver = webdriver.Chrome()
    id_selector = '.time a.tweet-timestamp'
    tweet_selector = 'li.js-stream-item'
    firsttweet_selector = 'first-tweet-wrapper'
    data_to_write = ""
    import time
    import sys
    print(str(_grabStart) + " through " + today + " is our interest for: " + name)
    #print("entering while loop")
    breakout = False
    while fetch_count <= fetch_sessions:
        try:
            #print("while loop triggered")
            #print(name)
            #print(_grabStart)
            #print(_grabEnd)
            #print(fetch_count)
            #print(fetch_sessions)
            #print(one_id)
            fetch_count = initiate_pull(name, _grabStart, _grabEnd, fetch_count, fetch_sessions, one_id, driver, tweet_selector, id_selector)
            #print("while fetch done")
            ####Incrament the values searched
            _grabStart += datetime.timedelta(days=days_per_query)
            _grabEnd = _grabStart + datetime.timedelta(days=days_per_query)
            #print("fetch count end count " + str(fetch_count))
        except:
            print("EXCEPTION ERROR END EXCEPTION ERROR END")
            e = sys.exc_info()[0]
            print("EXCEPTION ERROR END EXCEPTION ERROR")
            print( "Error: %s" % e )
            driver.quit()
            for proc in psutil.process_iter():
                # check whether the process name matches
                if proc.name() == PROCNAME:
                    proc.kill()
            #sleep (300)
            breakout = True
            break
    if breakout == True:
        #break
        return

    #print("Escaped from while loop")
    end_timer = time.time()
    total_t = end_timer - start_timer
    #print(str("%.0f" % ((total_t)/60)) + " minutes taken. to add " + fetched_days + " days. " + str(len(data_to_write)) + " tweets in the file of " + str(name) )
    print(str("%.0f" % ((total_t)/60)) + " minutes taken to update the file of " + str(name) )
    driver.quit()



















############Update to fetch specific user based on oldest _starDate
#### Retrieve data from DB on existing user
for another_user in all_data:
    start_timer = time.time()
    name = str(dict(another_user)['screen_name'])
    print(name)
    one_id = (dict(another_user)['id_str'])
    #print(one_id)
    #print(type(one_id))
    working_id = id_collection.find({'id_str': one_id})
    found = working_id.count()


    if found != 1:    #### If user is not in DB once then present an error
        print ("Error with user twitter id: " +str(one_id))
        if found == 0:
            print("Error note: ID not in DB despite earlier attempt to add it")
        else:
            print ("Error note: ID in the DB more than once")  #input("Press Enter to continue")
    else:    #### Existing user access found once, fetch their last tweet capture dates
        #print("we have a user to work on, line 490") #
        for x in working_id:  #for x in id_collection.find(({'id_str': one_id})):
            diction = x
            name = diction['screen_name']
            #print(name)

            #datetime.date(str(tday))
            twitter_ids_filename = 'tweet_ids_' + name+'.json'
            #print(str((list_dir + twitter_ids_filename)))
            #print(str(exists(list_dir + twitter_ids_filename)))
            ####if 1=2
        ####THIS IS FOR SKIPPING AHEAD TO NEW ADDITIONS
            if list_host == "NEW":
                print("NEW condition applied: Only Scrapping users which do not have an existing .json")
                if (exists(list_dir + twitter_ids_filename)):
                    pass
                else:
                    action_loop()
            else:
                action_loop()
