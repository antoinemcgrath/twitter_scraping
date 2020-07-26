#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################


#### Tips on using Twitters Search API:
#Limit your searches to 10 keywords and operators
#The Search API is not a complete index of all Tweets, but instead an index of recent Tweets
#The index includes between 6-9 days of Tweets
account_list = ["tassagency_en","RT_com","SputnikInt"]
term_list = ["congress"]


#### Import Python Packages
import tweepy
import json


#### Definition to Fetch Twitter api keys
#### If you do not have Twitter API keys visit developer.twitter.com/en/apps
#### Note accidental abuse of their API can result in a frozen account
#### Consider creating API keys from an account that is not your primary
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


#### Search each account for each term
print("Searching")
all_results =[]
for account in account_list: #For each account listed in accoun_list
    for term in term_list: #For each term listed in term_list
        search_results = None
        search_phrase = str(term + " from:" + account) #Create search phrase
        print(search_phrase) #Print the search phrase being requested
        search_results = api.search(search_phrase) #Search Twitter API for phrase
        if search_results is not None: #If result found add to list all_results
            for a_result in search_results:
                all_results.append(a_result)
        else:
            pass #If no result found generate reloop for new phrase and search


print("Found ", len(all_results), " positive results")

#### Printing positive Results
print("\n", "Time, Screen_name, Tweet_id, Favorites, Retweets, Retweeters")
for one in all_results:
    retweeters = [] #Creates an empty list named retweeters
    text = ""
    for status in api.retweets(one.id): #Creates a list of all the public retweeters
        retweeters.append(str(status.user.screen_name))
    text = one.text.replace('\n', ' ').replace('\r', '') #Removes line breaks from tweets
    print(one.created_at,  one._json['user']['screen_name'], one.id, one._json['retweet_count'], one._json['favorite_count'], retweeters, text, "\n")













