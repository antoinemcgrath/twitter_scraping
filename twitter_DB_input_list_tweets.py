# Rapid twitter viewer
import logging
#logging.basicConfig(filename='python_debug.log',level=logging.DEBUG) #Stores all runs
logging.basicConfig(filename='python_debug.log', filemode='w', level=logging.DEBUG) #Stores last run
#logging.debug('')#logging.info('')#logging.warning('')
import re
import os
import os.path
from time import sleep
import json
driver = None
from selenium.webdriver.chrome.options import Options

import urllib
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.command import Command


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




twitter_user = "AGreenDCBike"
tw_lists = ["candidates", "us-ca-assembly", "us-ca-bill"]




def generate_url(twitter_user, tw_list):
    #https://twitter.com/AGreenDCBike/lists/us-ca-assembly
    url = "https://twitter.com/" + twitter_user + "/lists/" + tw_list
    return(url)


'''
for tw_list in tw_lists:


    count = 0
    try:
        #API.list_timeline(owner, slug[, since_id][, max_id][, per_page][, page])
        twrecents = api.list_timeline(owner_screen_name=twitter_user, slug=tw_list, count=150)
        for tweet in twrecents:
            count = count + 1
            print (count, tweet.id_str, tweet.created_at, tweet.text)
        #api.get_list(slug=tw_list_id, owner_screen_name=twitter_user)
    except tweepy.error.TweepError as e:
        print ("Tweepy Error")
        print (e)



# General Stream Search # for tweet in tweepy.Cursor(api.search, q="google", rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(200):
# List search #
##### api.rate_limit_status()

count = 0
for tweet in tweepy.Cursor(api.list_timeline, q="google", owner_screen_name=twitter_user, slug=tw_list_id, rpp=100, count=100, result_type="recent", include_entities=True, lang="en").items(5000):
    count = count + 1

    print (count, tweet.created_at, tweet.text)
'''



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
        extradelay = extradelay + extradelay
        print("Sleeping for " + str(extradelay))
        sleep(extradelay)

    else:
        #print ("Delaying")
        #delay = (1+ 1000/(random.getrandbits(12)))
        delay = (1)
        sleep(delay)
        #print("scraping0 updating +10 dbbbbbbbbbb     " + (str(d2)))

        #### Scroll through page load page grab tweet IDs
        try:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            print("scroll")
            sleep(delay)
            #print("trying to found tweets")
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            for found in found_tweets:
                print(found)
            for tweet in found_tweets:
                #print("Escaping scraping 1 loop")
                try:
                    id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                    print(id)
                    ids.append(id)
                    print(str(len(ids)) + " :id length")
                except StaleElementReferenceException as e:
                    print('lost element reference', tweet)
            #print("scraping1")
            increment = 38
            while len(found_tweets) >= increment:
                #print('Loading page to load more tweets')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                print("scroll")
                sleep(delay)
                found_tweets = driver.find_elements_by_css_selector(tweet_selector)
                for tweet in found_tweets:
                    #print("Escaping scraping 1 loop")
                    try:
                        id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                        print(id)
                        ids.append(id)
                        print(str(len(ids)) + " :id length")
                    except StaleElementReferenceException as e:
                        print('lost element reference', tweet)
                increment += 10
            print('{} tweets fetched'.format(len(found_tweets)))
            #print("scraping2")
        except NoSuchElementException:
            try:   ##### Write twitter IDs to ID list json files
                #print("Open file if exists")
                with open(list_dir + twitter_ids_filename) as f:
                    all_ids = ids + json.load(f)
                    data_to_write = list(set(all_ids))
            except FileNotFoundError:
                #print("FILE DOES NOT EXIST, creating file")
                all_ids = ids
                data_to_write = list(set(all_ids))
            print('no tweets found')
            pass


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


def initiate_pull(driver, tweet_selector, tw_lists, id_selector):
    #print("F0 Initiating Pull Loop")
    for tw_list in tw_lists:
        url = generate_url(twitter_user, tw_list)
        print (url)
        fetch_tweets(url, driver, tweet_selector, id_selector)

def action_loop():
    chrome_options = Options() ##Note woah selenium extensions enabling https://stackoverflow.com/questions/16511384/using-extensions-with-selenium-python
    chrome_options.add_argument('--dns-prefetch-disable') ##options are Safari() Chrome() Firefox() Safari()
    driver = Chrome(chrome_options=chrome_options) ##driver = webdriver.Chrome()
    id_selector = '.time a.tweet-timestamp'
    tweet_selector = 'li.js-stream-item'
    firsttweet_selector = 'first-tweet-wrapper'
    data_to_write = ""
    import time
    import sys
    #print("entering while loop")
    breakout = False
    fetch_count = initiate_pull(driver, tweet_selector, tw_lists, id_selector)

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
    #print(str("%.0f" % ((total_t)/60)) + " minutes taken. to add " + fetched_days + " days. " + str(len(data_to_write)) + " tweets in the file of " + str(name) )
    driver.quit()



twitter_ids_filename = 'tweet_ids_' + "tw_list_input" + '.json'
action_loop()
