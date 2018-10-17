#!/usr/bin/python3

###################################################################
#  Do not use any of the code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

#### It happens to all of us.
#### You get carried away following all those interesting Twitter accounts
#### Then one day you wake up and you are following 2k people you don't know
####
#### This script can help.
####
#### Run this code to unfollow (unfriend) those Twitter users who do not follow you back

import json
import tweepy
import time
import re
import Twitter_Tools

Keys = Twitter_Tools.get_api_keys()
#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
user = Keys['Owner']




#### Input words of interst
def get_search_terms():
    lines = []
    print("Enter required keywords of interest")
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    interests1 = lines
    lines = []
    print("Enter a second list of required keywords of interest")
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    interests2 = lines
    lines = []
    return(interests1, interests2)


def create_search_list(interests1, interests2):
    search_list = []
    for one in interests1:
        for two in interests2:
            search_list.append(str('"'+ one +'" "' + two + '"'))
    return(search_list)


def search_users_bio(search_list):
    all_results = []
    search_count = 0
    user_count = 0
    for one_search in search_list:
        search_count += 1
        print("Search count:", search_count, "Search term:", one_search)
        found_users = [None] * 20
        another = -1
        if another is not 50: #A 50 page limit exists on API.search_users(q[, per_page][, page])
            if len(found_users) is 20:
                another += 1
                found_users = api.search_users(one_search, 20, another)
                for one_user in found_users:
                    if str(one_user.id) not in str(all_results):
                        user_count += 1
                        print(user_count, "https://www.twitter.com/"+str(one_user.screen_name), one_user.description)
                        all_results.append(one_user)
                time.sleep(1*1*3) #hrs*mins*secs
    return(all_results)


def create_list(user, list_name):
    description = input("Description of new list\n")
    bridge = "Keywords:"
    if len(description) > 100:
        description = description[:97]+"..."
    else:
        pass
    mode = input("public or private?\n")
    api.create_list(list_name, mode, description)



def if_no_list_create(user):
    list_name = input("Name of list to be created name (must start with alpha character and not contain special characters)\n")
    list_name = list_name.replace("_","-")
    list_of_lists = api.lists_all()
    for one_list in list_of_lists:
        if list_name == one_list.name:
            print("List exists")
            break
    create_list(user, list_name)
    return(list_name)


def add_to_list(user, list_name, all_results):
    for one in all_results:
        try:
            api.add_list_member(user_id=one.id, slug=list_name, owner_screen_name=user)
            time.sleep(1*1*3) #hrs*mins*secs
        except tweepy.error.TweepError as e:
            Twitter_Tools.twitter_rates(api)
            print (e.reason)
            #time.sleep(10800) #3hrs

#### Execute search workflow
interests1, interests2 = get_search_terms()
search_list = create_search_list(interests1, interests2)
all_results = search_users_bio(search_list)

#### Visit search results
print("Number of unique results:", len(all_results))


response = Twitter_Tools.query_yes_no("Do you want to add these results a twitter list?", "no")
if response == True: #return value is True for "yes" or False for "no"
    list_name = if_no_list_create(user)
    add_to_list(user, list_name, all_results)
else:
    pass

print("Completed")
Twitter_Tools.twitter_rates(api)




