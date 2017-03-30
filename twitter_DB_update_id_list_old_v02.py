#cd ~/.GITS/twitter_scrapping
#python3 scrape.py

#open up scrape.py and edit the user, start, and end variables (and save the file)
#all_ids.json (master file with all each tweet id)

#python3 get_metadata.py
#this will get metadata for every tweet id in all_ids.json
#username.json (master file with all metadata)
#username.zip (a zipped file of the master file with all metadata)
#username_short.json (smaller master file with relevant metadata fields)
#username.csv (csv version of the smaller master file)



#-- Brendan is great https://github.com/bpb27/twitter_scraping

#--For best results start with music http://www.djdaywalk.com/mixes/

#--Allow remote automation in your safari (v10+)
##Ensure that the Develop menu is available. It can be turned on by opening Safari preferences (Safari > Preferences in the menu bar), going to the Advanced tab, and ensuring that the Show Develop menu in menu bar checkbox is checked.
##Enable Remote Automation in the Develop menu. This is toggled via Develop > Allow Remote Automation in the menu bar.
##Authorize safaridriver to launch the webdriverd service which hosts the local web server. To permit this, run /usr/bin/safaridriver once manually and complete the authentication prompt.

#--Or Chrome Driver https://sites.google.com/a/chromium.org/chromedriver/downloads
##MAC:brew install chromedriver       Ubuntu: sudo apt-get install chromium-browser  https://christopher.su/2015/selenium-chromedriver-ubuntu/


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import json
import datetime
from datetime import date



# edit these three variables
user = 'realdonaldtrump'
start = datetime.date(2011, 1, 1)  # year, month, day
end = datetime.date(2017, 11, 11)  # year, month, day
#end = (date.today())

# only edit these if you're having problems
delay = 1  # time to wait on each page load before reading the page
driver = webdriver.Chrome()  # options are Safari() Chrome() Firefox() Safari()
##Note woah selenium extensions enabling https://stackoverflow.com/questions/16511384/using-extensions-with-selenium-python

# don't mess with this stuff
twitter_ids_filename = 'all_ids.json'
days = (end - start).days + 1
id_selector = '.time a.tweet-timestamp'
tweet_selector = 'li.js-stream-item'
firsttweet_selector = 'first-tweet-wrapper'

user = user.lower()
ids = []


def first_url():
    p1 = 'https://discover.twitter.com/first-tweet#' + user
    return p1

def first_tweet_id():
    # uses first_url def
    firsturl = first_url()
    #print(firsturl)
    driver.get(firsturl)
    sleep(delay)

    try:
        #driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #sleep(delay)
        found_tweets = driver.find_elements_by_id("twitter-widget-1")
        for tweet in found_tweets:
            try:
                first_id = tweet.get_attribute('data-tweet-id')
                return (first_id)
            except StaleElementReferenceException as e:
                print('lost element reference, no start tweet found', tweet)
    except NoSuchElementException:
        print('no start tweet found')

#firsttweetid = first_tweet_id()
#print (firsttweetid)






def format_day(date):
    day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    year = str(date.year)
    return '-'.join([year, month, day])

def form_url(since, until):
    p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
    p2 =  user + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
    return p1 + p2

def increment_day(date, i):
    return date + datetime.timedelta(days=i)

for day in range(days):
    d1 = format_day(increment_day(start, 0))
    d2 = format_day(increment_day(start, 1))
    url = form_url(d1, d2)
    #print(url)
    #print(d1)
    driver.get(url)
    sleep(delay)

    try:
        found_tweets = driver.find_elements_by_css_selector(tweet_selector)
        increment = 10

        while len(found_tweets) >= increment:
            print('scrolling down to load more tweets')
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(delay)
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            increment += 10

        print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))

        for tweet in found_tweets:
            try:
                id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                ids.append(id)
            except StaleElementReferenceException as e:
                print('lost element reference', tweet)

    except NoSuchElementException:
        #print('no tweets on this day')
        pass

    start = increment_day(start, 1)


try:
    with open(twitter_ids_filename) as f:
        all_ids = ids + json.load(f)
        data_to_write = list(set(all_ids))
        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(data_to_write))
except FileNotFoundError:
    with open(twitter_ids_filename, 'w') as f:
        all_ids = ids
        data_to_write = list(set(all_ids))
        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(data_to_write))

with open(twitter_ids_filename, 'w') as outfile:
    json.dump(data_to_write, outfile)

print('all done here')
driver.close()
