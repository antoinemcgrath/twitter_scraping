"extendSTART", "extendNewSTART", "New Start", "armscontrol", "arms control", "nuclearban", "noarmsrace", "nuclear", "new arms race", "nuclearproliferation", "nuclear proliferation"
@tassagency_en @RT_com @SputnikInt


("extendSTART" OR "extendNewSTART" OR "New OR Start" OR "armscontrol" OR "arms OR control" OR "nuclearban" OR "noarmsrace" OR "nuclear" OR "new OR arms OR race" OR "nuclearproliferation" OR "nuclear OR proliferation") (from:tassagency_en OR from:RT_com OR from:SputnikInt) until:2020-07-04 since:2020-06-20
https://twitter.com/search?q=(%22extendSTART%22%20OR%20%22extendNewSTART%22%20OR%20%22New%20OR%20Start%22%20OR%20%22armscontrol%22%20OR%20%22arms%20OR%20control%22%20OR%20%22nuclearban%22%20OR%20%22noarmsrace%22%20OR%20%22nuclear%22%20OR%20%22new%20OR%20arms%20OR%20race%22%20OR%20%22nuclearproliferation%22%20OR%20%22nuclear%20OR%20proliferation%22)%20(from%3Atassagency_en%20OR%20from%3ART_com%20OR%20from%3ASputnikInt)%20until%3A2020-07-04%20since%3A2020-06-20&src=typed_query


twitterscraper Trump -l 1000 -bd 2020-06-20 -ed 2020-07-04 -o tweets.json
twitterscraper "Blockchain from:VitalikButerin" -o blockchain_tweets.json -l 1000


account_list = ["tassagency_en","RT_com","SputnikInt"]
term_list = ["extendSTART", "extendNewSTART", "New Start", "armscontrol", "arms control", "nuclearban", "noarmsrace", "nuclear", "new arms race", "nuclearproliferation", "nuclear proliferation"]

print("Searching")
all_results =[]
for account in account_list: #For each account listed in accoun_list
    for term in term_list: #For each term listed in term_list
        search_results = None
        search_phrase = str(term + " from:" + account) #Create search phrase
        print(search_phrase) #Print the search phrase being requested

        for tweet in query_tweets(

            tweet.tweet_id, tweet.text
        search_results = api.search(search_phrase) #Search Twitter API for phrase
        if search_results is not None: #If result found add to list all_results
            for a_result in search_results:
                all_results.append(a_result)
        else:
            pass #If no result found generate reloop for new phrase and search

import pandas as pd
import tweepy
import json



#for loop to interate through our city list and scrape Twitter for a selection of targeted key words
for account in account_list:
    df_tweets = pd.DataFrame(columns=['id','text','timestamp','user','location'])
tweet_list = query_tweets(f'("extendSTART" OR "extendNewSTART" OR "New OR Start" OR "armscontrol" OR "arms OR control" OR "nuclearban" OR "noarmsrace" OR "nuclear" OR "new OR arms OR race" OR "nuclearproliferation" OR "nuclear OR proliferation" -filter:retweets', "from:" + account
                          begindate = datetime.date(2020,6,20),
                          enddate = datetime.date(2020,7,4),
                          poolsize = 10)



df_tweets = pd.DataFrame(columns=['id','text','timestamp','screen_name','retweets','retweeters'])
#print(tweet.timestamp, tweet.tweet_id, tweet.username, text)
for row, tweet in enumerate(tweet_list):
    retweeters = []
    for status in api.retweets(tweet.tweet_id, wait_on_rate_limit=True): #Creates a list of all the public retweeters
        retweeters.append(str(status.user.screen_name))
#for row in tweet_list:
    text = tweet.text.replace('\n', ' ').replace('\r', '')
    df_tweets.loc[row,'id'] = tweet.tweet_id
    df_tweets.loc[row,'text'] = text
    df_tweets.loc[row,'timestamp'] = tweet.timestamp
    df_tweets.loc[row,'screen_name'] = tweet.screen_name
    df_tweets.loc[row,'retweets'] = tweet.retweets
    df_tweets.loc[row,'retweeters'] = retweeters


#tweet.likes tweet.retweets

df_tweets.to_csv(f'/Users/macbook/Desktop/results_tweets.csv')




def get_api_keys():
    #### Set Twitter API key dictionary
    try:    #### Attempt to load API keys file
        keys_json = json.load(open('/usr/local/keys.json'))
        #### Specify key dictionary wanted (generally [Platform][User][API])
        Keys = keys_json["Twitter"]["ClimateCong_Bot"]["ClimatePolitics"]
    except Exception as e:
        er = e
        if er.errno == 2: #File not found enter key dictionary values manually
            print("\nNo twitter API key was found in /usr/local/keys.json\n",
                 "Acquire an API key at https://apps.twitter.com/\n",
                 "to supply key manually press Enter\n")
            Keys = {}
            Keys['Consumer Key (API Key)'] = input('Enter the Twitter API Consumer Key\n')
            Keys['Consumer Secret (API Secret)'] = input('Enter the Twitter API Consumer Secret Key\n')
            Keys['Access Token'] = input('Enter the Twitter API Access Token\n')
            Keys['Access Token Secret'] = input('Enter the Twitter API Access Token Secret\n')
            Keys['Owner'] = input('Enter your Twitter username associated with the API keys\n')
        else:
            print(e)
    return(Keys)


#### Login to twitter API
Keys = get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
list_owner = Keys['Owner']



for one in all_results:
    retweeters = [] #Creates an empty list named retweeters
    text = ""
    for status in api.retweets(one.id): #Creates a list of all the public retweeters
        retweeters.append(str(status.user.screen_name))

df_tweets.to_csv(f'/Users/macbook/Desktop/results_tweets2.csv')



1277892883572559873
1277950012039684096



from lxml.html import parse
from urllib.request import urlopen




import urllib2
import re

def get_user_ids_of_post_likes(post_id):
    try:
        json_data = urllib2.urlopen('https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read()
        found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
        unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
        return unique_ids
    except:
        return False


print(get_user_ids_of_post_likes(1280056047646978050))

from lxml.html import parse


#returns list(retweet users),list(favorite users) for a given screen_name and status_id
def get_twitter_user_rts_and_favs(screen_name, status_id):
    url = urllib2.urlopen('https://twitter.com/' + screen_name + '/status/' + status_id)
    root = parse(url).getroot()
    num_rts = 0
    num_favs = 0
    rt_users = []
    fav_users = []
    for ul in root.find_class('stats'):
        for li in ul.cssselect('li'):
            cls_name = li.attrib['class']
            if cls_name.find('retweet') >= 0:
                num_rts = int(li.cssselect('a')[0].attrib['data-tweet-stat-count'])
            elif cls_name.find('favorit') >= 0:
                num_favs = int(li.cssselect('a')[0].attrib['data-tweet-stat-count'])
            elif cls_name.find('avatar') >= 0 or cls_name.find('face-pile') >= 0:#else face-plant
                for users in li.cssselect('a'):#apparently, favs are listed before retweets, but the retweet summary's listed before the fav summary
                    #if in doubt you can take the difference of returned uids here with retweet uids from the official api
                    if num_favs > 0:#num_rt > 0:
                        #num_rts -= 1
                        num_favs -= 1
                        #rt_users.append(users.attrib['data-user-id'])
                        fav_users.append(users.attrib['data-user-id'])
                    else:
                        #fav_users.append(users.attrib['data-user-id'])
                        rt_users.append(users.attrib['data-user-id'])
        return rt_users, fav_users

https://twitter.com/KKertysova/status/1280056047646978050
#example
if __name__ == '__main__':
    print(get_twitter_user_rts_and_favs('KKertysova', '1280056047646978050'))