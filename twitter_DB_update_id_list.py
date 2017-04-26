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
days_per_query = 364

#### Arrising Errors
#selenium.common.exceptions.TimeoutException: Message: timeout: cannot determine loading status
import urllib
import socket
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.command import Command
##selenium.common.exceptions.WebDriverException: Message: unknown error: failed to close window in 20 seconds
#Solution detect if still active after end command if so reinstruct
def get_status(driver):
    print("Loop1")
    try:
        driver.execute(Command.STATUS)
        driver.quit()
        get_status(driver)
        return "Alive"
    except ConnectionRefusedError:
        return "Connection refused"
    except (socket.error, urllib.CannotSendRequest):
        return "Dead"






#
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
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv"
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv" #ck

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
    print("Loop2")
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
def get_twitter_keys(twitterKEYfile):
    print("Loop3")
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
    return (api)




api = get_twitter_keys(twitterKEYfile)

#### 2DO (Add pull from twitter API of list)
#### Retrieve a list of users from twitter lists and add them to the DB if they do not exists
def get_twit_list():
    print("Loop4")
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
    print("Loop5")
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
            id_collection.update({'id': one_id},{'$set' : {"_accountStart":_accountStart}}) #FAILURE Did not ASSIGN DB VALUE TYPE AS 9 (DATE) id_collection.update({'id': one_id},{'$set' : {"_accountStart": {$field:9  int(_accountStart)}  }}) ##https://docs.mongodb.com/manual/reference/operator/query/type/
            id_collection.update({'id': one_id},{'$set' : {"_grabStart":_grabStart}})
            #id_collection.update({'id': one_id},{'$set' : {"_grabEnd":_grabEnd}})#collection.find({"$text": {"$search": str("realDonaldTrump"), '$caseSensitive': False}}).count()        #collection.find({ '$text': { '$search': 'realDonaldTrump', '$caseSensitive': True } }).count()
            ###for x in id_collection.find(({'id': one_id})):
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

print("here line 198 now")
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
    print("Loop6")
    print("getting db  user list to update")
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
    print("(F1 Generate URL Loop")      
    url_A = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    url_B =  name + '%20since%3A' + str(_grabStart) + '%20until%3A' + str(_grabEnd) + 'include%3Aretweets&src=typd'
    url = url_A + url_B
    return (url)
      
def fetch_tweets(url):
    print("(F2 Fetch Tweets Loop")      
    print(str(url))
    ids = []
    
    #### Detect Blocking
    try:
        driver.get(url)
    except TimeoutException as ex:
        print(ex.Message)
        driver.navigate().refresh()

    page_source = driver.page_source  
    if page_source.find(".block") > 0:
        mydate = datetime.datetime.now()
        print(page_source)
        print (mydate.strftime('Blocked at is %d %B'))
        extradelay = extradelay + extradelay
        print("Sleeping for " + str(extradelay))
        sleep(extradelay)
    else:
        print ("Delaying")
        #delay = (1+ 1000/(random.getrandbits(12)))
        delay = (1.02)
        sleep(delay)
        #print("scraping0 updating +10 dbbbbbbbbbb     " + (str(d2)))
        #id_collection.update({'id': one_id},{'$set' : {"_grabStart":d2}})
        #id_collection.update({'id': one_id},{'$set' : {"_grabEnd":d2}})
       
        #### Scroll through page load page grab tweet IDs
        try:
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            print("scraping1")
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
            print("scraping2")
        except NoSuchElementException:
            pass #print('no tweets on this day')            
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


def update_progress(_grabStart, _grabEnd, fetch_count, fetch_sessions):
    print("F3 Update DB/Incrament Loop")     
    if str(_grabStart) < str(tday): 
        print("Writing _grabStart into DB start")
        print(str(_grabStart))
        print(str(tday))
        id_collection.update({'id': one_id},{'$set' : {"_grabStart":str(_grabStart)}}) ##Updates id_DB to reflect latest crawl
    else:
        print("Writing tday into DB start")
        print(str(_grabStart))
        print(str(tday))
        id_collection.update({'id': one_id},{'$set' : {"_grabStart":str(tday)}}) ##Updates id_DB to reflect latest crawl
    _grabStart += datetime.timedelta(days=days_per_query)
    _grabEnd = _grabStart + datetime.timedelta(days=days_per_query)
    fetch_count += 1
    print (str(fetch_sessions) + " fetches needed " + str(fetch_count) + " completed") 
    return(fetch_count)   

def initiate_pull(name, _grabStart, _grabEnd, fetch_count, fetch_sessions):    
    print("(F0 Initiating Pull Loop")               
    url = generate_url(name, _grabStart, _grabEnd)
    fetch_tweets(url)
    fetch_count = update_progress(_grabStart, _grabEnd, fetch_count, fetch_sessions)
    return(fetch_count)    
    

############Update to fetch specific user based on oldest _starDate
#### Retrieve data from DB on existing user
for another_user in all_data:
    start_timer = time.time()
    name = str(dict(another_user)['screen_name'])
    one_id = (dict(another_user)['id'])   #print(one_id)
    working_id = id_collection.find({'id': one_id})
    found = working_id.count()
    if found != 1:    #### If user is not in DB once then present an error
        print ("Error with user twitter id: " +str(one_id))
        if found == 0:
            print("Error note: ID not in DB despite earlier attempt to add it")
        else:
            print ("Error note: ID in the DB more than once")  #input("Press Enter to continue")
    else:    #### Existing user access found once, fetch their last tweet capture dates
        print("we have a user to work on, line 380") #
        for x in working_id:  #for x in id_collection.find(({'id': one_id})):
            diction = x
            name = diction['screen_name']
            #print(name)
            
            _grabStart = dt.date(dt.strptime(diction['_grabStart'], '%Y-%m-%d'))
            _grabEnd = _grabStart + datetime.timedelta(days=days_per_query)
            
            #datetime.date(str(tday))
            twitter_ids_filename = 'tweet_ids_' + name+'.json'
            days = (tday - _grabStart).days + 1
            fetch_days = str(days)
            fetch_sessions = math.ceil(float(int(fetch_days)/days_per_query))
            fetch_count = 0
            print( name + " Days to fetch: " + str(fetch_days) + " Fetch sessions required: " + str(fetch_sessions) + " Current fetch count: " + str(fetch_count))
            print ("Fetched span: " + str(_grabStart) + " " + str(_grabEnd))  

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
            print("entering while loop")
            while fetch_count <= fetch_sessions:
                #print("while loop triggered")
                fetch_count = initiate_pull(name, _grabStart, _grabEnd, fetch_count, fetch_sessions) 
                print(str(fetch_count))
            print("WHILE LOOP IS DONE")
            print("ending timerrrrrrrrrrrrrrrrrrrr")
            end_timer = time.time()
            total_t = end_timer - start_timer
            #print(str("%.0f" % ((total_t)/60)) + " minutes taken. to add " + fetched_days + " days. " + str(len(data_to_write)) + " tweets in the file of " + str(name) )
            print(str("%.0f" % ((total_t)/60)) + " minutes taken to update the file of " + str(name) )
            
            driver.quit()
            print(get_status(driver))
            ####tday-_grabStart

            #_grabStart = dt.date(dt.strptime(diction['_grabStart'], '%Y-%m-%d'))
            #_grabEnd = dt.date(dt.strptime(diction['_grabEnd'], '%Y-%m-%d'))
            #days_to_fetch = int(str(tday-_grabStart).split(" ")[0])
            #print("Fetching : " + days_to_fetch + " days.
            #print("Starting with: " + str(_grabStart))
            #print("Through: " + today)





   
    


  
   




