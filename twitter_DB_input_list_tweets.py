# Rapid twitter viewer
import os
import os.path

#Import Twitter
import tweepy #http://www.tweepy.org/
from tweepy import TweepError
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

twitter_user = "AGreenDCBike"
tw_lists = ["candidates", "us-ca-assembly", "us-ca-bill"]

#Setup Twitter
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter01.csv" #
twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter02.csv" #AGreenDCBike
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter03.csv" #
#twitterKEYfile = os.path.expanduser('~') + "/.invisible/twitter05.csv" #

def get_twitter_keys(twitterKEYfile):
    #print("Loop3")
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

#End Twitter Setup


for a_list in tw_lists:


count = 0
try:
    #API.list_timeline(owner, slug[, since_id][, max_id][, per_page][, page])
    twrecents = api.list_timeline(owner_screen_name=twitter_user, slug=a_list, count=150)
    for tweet in twrecents:
        count = count + 1
        print (count, id_str, tweet.created_at, tweet.text)
    #api.get_list(slug=tw_list_id, owner_screen_name=twitter_user)
except tweepy.error.TweepError as e:
    print ("Tweepy Error")
    print (e)



# General Stream Search # for tweet in tweepy.Cursor(api.search, q="google", rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(200):
# List search #
count = 0
for tweet in tweepy.Cursor(api.list_timeline, q="google", owner_screen_name=twitter_user, slug=tw_list_id, rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(30):
    count = count + 1
    print (count, tweet.created_at, tweet.text)
