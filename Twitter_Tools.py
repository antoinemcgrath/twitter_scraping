#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

import json
import time
import random


#### Fetch Twitter api keys
def get_api_keys():
    #### Set Twitter API key dictionary
    try:    #### Attempt to load API keys file
        keys_json = json.load(open('/usr/local/keys.json'))
        #### Specify key dictionary wanted (generally [Platform][User][API])
        #Keys = keys_json["Twitter"]["ClimateCong_Bot"]["ClimatePolitics"]
        Keys = keys_json["Twitter"]["AGreenDCBike"]["HearHerVoice"]
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


#### Fetch Mashape api keys
def get_mashape_api_keys():
    #### Set Twitter API key dictionary
    try:    #### Attempt to load API keys file
        keys_json = json.load(open('/usr/local/keys.json'))
        #### Specify key dictionary wanted (generally [Platform][User][API])
        mashape_key = keys_json["mashape_key"]
    except Exception as e:
        er = e
        if er.errno == 2: #File not found enter key dictionary values manually
            print("\nNo mashape API key was found in /usr/local/keys.json\n",
                 "Acquire an API key at Mashape\n",
                 "to supply key manually press Enter\n")
            mashape_key = input('Enter the Mashape API Key\n')
            print(e)
    return(mashape_key)


#### Define twitter rate determining loop
def twitter_rates(api):
    stats = api.rate_limit_status()  #stats['resources'].keys()
    for akey in stats['resources'].keys():
        if type(stats['resources'][akey]) == dict:
            for anotherkey in stats['resources'][akey].keys():
                if type(stats['resources'][akey][anotherkey]) == dict:
                    #print(akey, anotherkey, stats['resources'][akey][anotherkey])
                    limit = (stats['resources'][akey][anotherkey]['limit'])
                    remaining = (stats['resources'][akey][anotherkey]['remaining'])
                    used = limit - remaining
                    if used != 0:
                        print("  Twitter API used:", used, "requests used,", remaining, "remaining, for API queries to", anotherkey)
                    else:
                        pass
                else:
                    pass  #print("Passing")  #stats['resources'][akey]
        else:
            print(akey, stats['resources'][akey])
            print(stats['resources'][akey].keys())
            limit = (stats['resources'][akey]['limit'])
            remaining = (stats['resources'][akey]['remaining'])
            used = limit - remaining
            if used != 0:
                print("  Twitter API:", used, "requests used,", remaining, "remaining, for API queries to", akey)
                pass


#### Like tweets made by a user
def like_users_tweets(a_user_id, like_this_many, api):
    #Note that this checks a maximum of 40 users tweets, can be extended to 200
    path = "backups/"+str("__tweets_autoliked.txt")
    fresh_tweets = api.user_timeline(a_user_id, count=40)
    liked_count = 0
    for tweet in fresh_tweets:
        if a_user_id == tweet.user.id:
            if tweet.text[0:4] != "RT @":
                if tweet.in_reply_to_screen_name == None:
                    tweet_url = (str(a_user_id) + "," + str(tweet.id) + ",https://twitter.com/" + str(tweet.user.screen_name) + "/status/" + str(tweet.id))
                    tweet.favorite()
                    with open(path,"a+") as file:
                        file.write(str(tweet_url) + '\n')
                    liked_count += 1
                    print("like count", liked_count, tweet_url)
                    time.sleep(random.uniform(1,40))
                    if liked_count == like_this_many:
                        break


#### Unlike automated tweets made by a user
def unlike_users_tweets(a_user_id, api):
    path = "backups/"+str("__tweets_autoliked.txt")
    with open(path,"r") as file:
        lines = file.readlines()
        tweets_to_unlike = ([line for line in file if 'Richard' in line])
        for a_line in tweets_to_unlike:
            unlike_id = a_line.split(",")[1]
            try:
                api.destroy_favorite(unlike_id)
                finpath = "backups/"+str("__tweets_autoliked_unliked.txt")
                with open(finpath,"a+") as finfile:
                    finfile.write(a_line)
                print(unlike_id, "DESTROYED")
                time.sleep(random.uniform(1,4))
                lines.remove(a_line)
            except:
                print("Failed to unlike", unlike_id)
                pass
    with open(path,"w") as file:
        for line in lines:
            file.write(line)
