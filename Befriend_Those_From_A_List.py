#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

#### A script for copying the twitter users you follow into one of your twitter lists
import json
import tweepy
import time
import re
import random
import Twitter_Tools
import os

records_dir = "./backups/"
like_this_many = 3 #The number of their tweets to like

Keys = Twitter_Tools.get_api_keys()


#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth)
user = Keys['Owner']

#### Specify list to befriend
url = input("Enter the URL of the list you would like to befriend\n") #leaders #favs-always-follow
list_owner = url.split("/")[3] #https://twitter.com/ShaunaCausey/lists/tech-journalists
list_name = url.split("/")[5] #ShaunaCausey tech-journalists

#### Get the list of users
#followers = api.followers_ids(user)
list1 = friends = api.friends_ids(user)
print("The number of users followed is: " +str(len(list1)))


#### Get list of user ids from those within the list of interest
listed = []
for page in tweepy.Cursor(api.list_members, list_owner, list_name, wait_on_rate_limit=True).pages():
    listed.extend(page)
    #time.sleep(2)
    #print(len(listed))
list2=[]
for one in listed:
    list2.append(one.id)

print("The number of users in " + list_owner +"'s list", list_name, "is: " +str(len(list2)))



#### Remove those user ids which are already in the list
a_befriend =  [x for x in list2 if x not in list1]
newfriends = str(len(a_befriend))
print("The number of users that are not allready followed: ", newfriends)

#### Get list of those recently interacted (followed/unfollowed/followed_me)
def recently_followed_or_followers():
    a = [name for name in os.listdir(records_dir) if name.endswith(".txt")]
    past_list =[]
    for one_f in a:
        past_list += [line.rstrip() for line in open(records_dir+one_f)]
        #print(len(past_list))
    return(past_list)

past_list = recently_followed_or_followers()


#### Remove those user ids which are already in the list
befriend =  [x for x in list2 if x not in past_list]
newfriends = str(len(befriend))
print("The number of users that are not allready followed: ", newfriends)



random.shuffle(befriend)

for newfriend in befriend:
    print(str(len(befriend)), "remaining friends to be added, of", newfriends, "total", end='\r')
    #print(newfriend)
    try:
        api.create_friendship(newfriend)
        befriend.remove(newfriend)
        Twitter_Tools.like_users_tweets(newfriend, like_this_many, api)
        time.sleep(random.uniform(1,180))
    except Exception as e:
        er = e
        if e.api_code in locals():
            if e.api_code == 160:
                print("Request to befriend made, pending approval")
                befriend.remove(newfriend)
            if e.api_code == 50:
                print("User not found")
                pass
        else:
            print(e)
            input("Press Enter to continue...")
            befriend.remove(newfriend)
            pass


print("Completed")
Twitter_Tools.twitter_rates(api)
sys.exit() #End app
