#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

# Rapid twitter viewer
import logging
#logging.basicConfig(filename='python_debug.log',level=logging.DEBUG) #Stores all runs
logging.basicConfig(filename='python_debug.log', filemode='w', level=logging.DEBUG) #Stores last run
#logging.debug('')#logging.info('')#logging.warning('')

import pytz # Timezone index For twitter to date formate conversion
import os
import os.path

#Import Twitter
import tweepy #http://www.tweepy.org/
from tweepy import TweepError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

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


import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
user = Keys['Owner']



auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
#End Twitter Setup


def generate_url(twitter_user, tw_list):
    #https://twitter.com/AGreenDCBike/lists/us-ca-assembly
    url = "https://twitter.com/" + twitter_user + "/lists/" + tw_list
    return(url)





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
        print (mydate.strftime('Blocked at is %d %B'))('US_CA_Senate', 'US_CA_Legislature_Latest_Actions', 'us-ca-senate', 'BotResource:US_CA_Hashes')

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
            #for found in found_tweets:
            #    print(found)
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
            increment = 10
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
<<<<<<< HEAD
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
=======
>>>>>>> 2f9a1ab763dfd2c42c1d7b2677fbcf84a095c632
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


def initiate_pull(driver, tweet_selector, tw_lists):
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
    fetch_count = initiate_pull(driver, tweet_selector, tw_lists)

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

## Date conversion
## datetime.strptime((t['created_at']),'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
