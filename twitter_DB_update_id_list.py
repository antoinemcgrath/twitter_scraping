#!/usr/bin/python


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
# python3 twitter_DB_update_id_list.py

# Compiles all tweet ids fetched from a users single day timeline & updates mongodb with the date completed
# Example of gnerated URL: https://twitter.com/search?f=tweets&vertical=default&q=from%3ABarackObama%20since%3A2016-03-14%20until%3A2016-03-15include%3Aretweets&src=typd


# ERRORS: After prolonged runs (~36hrs+) may start receiving twitter pages with no tweets. 
#         Activity is within twitter rate limit.
#         Potential browser error
#         Potential ISP problem
#         Possibly triggered by brief drop in internet




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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import tweepy #http://www.tweepy.org/
from tweepy import TweepError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
connection = c = MongoClient() #connection = c = MongoClient(localhost', '27017') #connection = Connection('localhost', '27017')
extradelay = 1

#### Arrising Errors
#selenium.common.exceptions.TimeoutException: Message: timeout: cannot determine loading status
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

##selenium.common.exceptions.WebDriverException: Message: unknown error: failed to close window in 20 seconds
#Solution detect if still active after end command if so reinstruct
import urllib
import socket
from selenium.webdriver.remote.command import Command
def get_status(driver):
    try:
        driver.execute(Command.STATUS)
        driver.quit()
        get_status(driver)
        return "Alive"
    except ConnectionRefusedError:
        return "Dead? connection refused"
    except (socket.error, urllib.CannotSendRequest):
        return "Dead"

#
#
#
####




#### Add users to DB from specified twitter group list
# For: https://twitter.com/cspan/lists/members-of-congress

list_host = 'AGreenDCBike'
list_name = 'climatepolitics-info'

#list_host = 'Pete_Weldy'
#list_name = 'california-dems'

#list_host = 'ericlinder'
#list_name = 'ca-assembly-members'

#list_host = 'apen4ej'
#list_name = 'california-state-senate'

#list_host = 'apiahf'
#list_name = 'ca-state-assembly'

#list_host = 'cspan'
#list_name = 'members-of-congress'
#list_name = 'foreign-leaders'
#list_name = 'governors'
#list_name = 'u-s-representatives'
#list_name = 'senators'

# For: https://twitter.com/AGreenDCBike/lists/us-gov
#list_host = 'AGreenDCBike'
#list_name = 'us-gov'

list_dir = "tweet_ids_2nd/"
#list_dir = "tweet_ids/" + list_host + "/" + list_name + "/"
if not os.path.exists(list_dir):
    os.makedirs(list_dir)

####Close existing webdriver activity
import psutil
PROCNAME = "chromedriver"
for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()


    


# The MongoDB connection info. This assumes your database name is Political and your collection name is tweets.
db = connection.Twitter #db.tweets.ensure_index("id", unique=True, dropDups=True)
db.politicians.ensure_index( "id", unique=True, dropDups=True )
collection = db.politicians

db.id_politicians.ensure_index( "id", unique=True, dropDups=True )
id_collection = db.id_politicians

#### tweet_count = db.politicians.count("id", exists= True)
#### print ("Total tweet count in DB is: " + str(tweet_count))


# Retrieve Twitter API credentials
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv"
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv" #ck
with open(twitterKEYfile, 'r') as f:
    e = f.read()
    keys = e.split(',')
    consumer_key = keys[0]  #consumer_key
    consumer_secret = keys[1]  #consumer_secret
    access_key = keys[2]  #access_key
    access_secret = keys[3]  #access_secret
# http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#### 2DO (Add pull from twitter API of list)
#### Retrieve a list of users from twitter lists and add them to the DB if they do not exists
def get_twit_list():
    twit_list = []
    twitter_pull = tweepy.Cursor(api.list_members, list_host, list_name).items()
    for user in twitter_pull:
        twit_list.append(user.screen_name)
    ####twit_list =  ['realDonaldTrump', 'BarackObama'] #Example list
    return (twit_list)
####
###input("Press Enter to retrieve users names from twitter list")
twit_list = get_twit_list()
print (str(twit_list))
print (len(twit_list))


#### Add new users from twit list to the DB (id collection)
def add_new_twit_list_members_to_db():


    all_data = []
    start = 0
    end = 100
    limit = len(twit_list)
   # print (limit)
    i = math.ceil(limit / 100)
   # print (i)

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
        #### New user add to DB
        if found == 0:
            print("Uploading new user " + name + " to db")
            user_add_count = user_add_count + 1
            id_collection.insert(a_user)
            Account_Start = (a_user)['created_at']
            _accountStart = _grabStart = _grabEnd = time.strftime('%Y-%-m-%-d', time.strptime(Account_Start,'%a %b %d %H:%M:%S +0000 %Y'))
            _db_itemcreated = _db_itemupdated = datetime.datetime.now()#collection.find({'id': one_id})        #= (a_user._json)['created_at']
            id_collection.update({'id': one_id},{'$set' : {"_accountStart":_accountStart}}) #MASSIVE FAILURE TO ASSIGN DB VALUE TYPE AS 9 (DATE) id_collection.update({'id': one_id},{'$set' : {"_accountStart": {$field:9  int(_accountStart)}  }}) ##https://docs.mongodb.com/manual/reference/operator/query/type/
            id_collection.update({'id': one_id},{'$set' : {"_grabStart":_grabStart}})
            id_collection.update({'id': one_id},{'$set' : {"_grabEnd":_grabEnd}})#collection.find({"$text": {"$search": str("realDonaldTrump"), '$caseSensitive': False}}).count()        #collection.find({ '$text': { '$search': 'realDonaldTrump', '$caseSensitive': True } }).count()
            ###for x in id_collection.find(({'id': one_id})):
            ###    diction = x
            ###    _grabStart = dt.date(dt.strptime(diction['_grabStart'], '%Y, %m, %d'))
            ###    _grabEnd = dt.date(dt.strptime(diction['_grabEnd'], '%Y, %m, %d'))
            pass
        else:
            pass
    print (str(user_add_count) + " new users were added to the DB")

####
#input("Press Enter to add new users to DB ")
add_new_twit_list_members_to_db()




#### Searc mongo return users who's dates are not today (tday)



#### Get DB list to update
def get_user_list():
    print("getting db  user list ot update")
    user_list = []
    #for x in id_collection.find({"_grabEnd": {'$ne': "2009-03-30" }},{"screen_name": 1}):
    for x in id_collection.find({"_grabEnd": {'$ne': today}},{"screen_name": 1}):#.sort({"_grabStart": -1}):
        diction = x
        user_list.append(diction['screen_name'])
    #print (user_list)
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

for go in range(i):
    print('Looking up users {} - {}'.format(start, end))
    sleep(6)  # needed to prevent hitting API rate limit
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




#### Retrieve data from DB on existing user
for another_user in all_data:
    start_timer = time.time()
    name = str(dict(another_user)['screen_name'])
    one_id = (dict(another_user)['id'])   #print(one_id)
    found = id_collection.find({'id': one_id}).count()

    #### If user is not in DB once then present an error
    if found != 1:
        print ("Error with user twitter id: " +str(one_id))
        if found == 0:
            print("Error note: ID not in DB despite earlier attempt to add it")
        else:
            print ("Error note: ID in the DB more than once")
        #input("Press Enter to continue")

    #### Existing user access found once, fetch their last tweet capture dates
    else:
        for x in id_collection.find(({'id': one_id})):
            diction = x
            _grabStart = dt.date(dt.strptime(diction['_grabStart'], '%Y-%m-%d'))
            _grabEnd = dt.date(dt.strptime(diction['_grabEnd'], '%Y-%m-%d'))
            print(str(_grabStart) + " through " + today + " is our interest for: " + diction['screen_name'])


    # Delay Generated later each loop ## delay = 1  # time to wait on each page load before reading the page
    #driver = webdriver.Chrome() ##Updated, imported earlier and with options # options are Safari() Chrome() Firefox() Safari()##Note woah selenium extensions enabling https://stackoverflow.com/questions/16511384/using-extensions-with-selenium-python
    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    driver = Chrome(chrome_options=chrome_options)

    
   
    
    #datetime.date(str(tday))
    twitter_ids_filename = 'tweet_ids_' + name+'.json'
    days = (tday - _grabStart).days + 1
    fetched_days = str(days) 
    #print( name + " Days to fetch: " + str(days))
    #input("Press Enter to continue")
    import time
    import sys


    id_selector = '.time a.tweet-timestamp'
    tweet_selector = 'li.js-stream-item'
    firsttweet_selector = 'first-tweet-wrapper'

    ids = []

    def format_day(date):
        day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
        month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
        year = str(date.year)
        return '-'.join([year, month, day])
    def form_url(since, until):
        p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
        p2 =  name + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
        return p1 + p2
    def increment_day(date, i):
        #from datetime import datetime, timedelta
        #print (datetime.timedelta(days=i))
        return date + datetime.timedelta(days=i)



    for day in range(days):
        d1 = format_day(increment_day(_grabStart, 0))
        d2 = format_day(increment_day(_grabStart, 1))
        url = form_url(d1, d2)
        #print("Fetch " + str(d1) + " through " + str(d2) + "  " + url)
        
        #### Detect Blocking
        try:
            driver.get(url)
        except TimeoutException as ex:
            print(ex.Message)
            driver.navigate().refresh()
   
   
        page_source = driver.page_source
        #print(page_source)
        if page_source.find(".block") > 0:
            mydate = datetime.datetime.now()
            print(page_source)
            print (mydate.strftime('Blocked at is %d %B'))
            extradelay = extradelay + extradelay
            print("Sleeping for " + str(extradelay))
            sleep(extradelay)
        else:
            #print ("all good")
    
            #delay = (1+ 1000/(random.getrandbits(12)))
            delay = (1.02)
            sleep(delay)
            id_collection.update({'id': one_id},{'$set' : {"_grabStart":d1}})
            id_collection.update({'id': one_id},{'$set' : {"_grabEnd":d2}})


            try:
                found_tweets = driver.find_elements_by_css_selector(tweet_selector)
                increment = 10
                while len(found_tweets) >= increment:
                    #print('Loading page to load more tweets')
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    sleep(delay)
                    found_tweets = driver.find_elements_by_css_selector(tweet_selector)
                    increment += 10

                #print('{} tweets fetched, {} total'.format(len(found_tweets), len(ids)))

                for tweet in found_tweets:
                    try:
                        id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                        ids.append(id)
                    except StaleElementReferenceException as e:
                        print('lost element reference', tweet)

            except NoSuchElementException:
                #print('no tweets on this day')
                pass
            _grabStart = increment_day(_grabStart, 1)

            try:
                with open(list_dir + twitter_ids_filename) as f:
                    all_ids = ids + json.load(f)
                    data_to_write = list(set(all_ids))
                    #print("Between " + str(d1) + " and " + str(d2) + " user tweeted " + str(len(found_tweets)) + " times. Total fetched from user in this session " + str(len(ids)) + ' Tweets in file: ', str(len(data_to_write)))
            except FileNotFoundError:
                with open(list_dir + twitter_ids_filename, 'w') as f:
                    all_ids = ids
                    data_to_write = list(set(all_ids))
                    #print("Between " + str(d1) + " and " + str(d2) + " user tweeted " + str(len(found_tweets)) + " times. Total fetched from user in this session " + str(len(ids)) + ' Tweets in file: ', str(len(data_to_write)))
            with open(list_dir + twitter_ids_filename, 'w') as outfile:
                json.dump(data_to_write, outfile)
    end_timer = time.time()
    total_t = end_timer - start_timer
    print(str("%.0f" % ((total_t)/60)) + " minutes taken to add " + fetched_days + " days. " + str(len(data_to_write)) + " tweets in the file of " + str(name) )
    #print(get_status(driver))#do not allow with driver.quit() in loop
    #driver.close()
    driver.quit()
    print(get_status(driver))


#print ("Political db tweet count is : " + str(tweet_count))

'''
Notes from a reviewer::
pyMongo uses datetime.datetime for dates
unless you're inserting datetime.datetime objects, they're not gonna be dates in the mongodb they're gonna be strings
it looks like _accountStart is a STRING, not a datetime object (see line 139 and 141)
_grabStart and _grabEnd are also strings

what's the purpose of the "if" statement on line 205
if the user isn't present in the database, will that be bad?
right, but i think that the script will crash after printing that error message because some vital variables (_grabStart, _grabEnd, etc.) are assigned only in the "else" case so i think you want a "continue" statement at the end of the "if" block like, if found != 1, print the error, then "continue" to skip that user and go onto the next one then you can delete the "else" and move that code into the main flow
in general it's good to have things like line 230, and 231, at the top of your file once especially cuz where they are right now results in that stuff being imported every loop iteration better to just import it once at the top
also the "format_day, "form_url" and "increment_day" functions should really be outside of that loop

Rewrite update code to occure after fetch code (for sake of clarity)
'''
