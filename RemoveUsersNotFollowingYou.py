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
api = tweepy.API(auth)
list_owner = Keys['Owner']

list_name = "a-2018-favs" #### If there is a list of users that you do not want to unfollow


#### Get list of friends IDs
friends = api.friends_ids(api.me().id)
print("Friend count:",len(friends))

#### Get list of followers IDs
followers = api.followers_ids(api.me().id)
print("Follower count:",len(followers))


#### Create a list friends that do not follow back
notfollowingback = [x for x in friends if x not in followers]
print("Friends not following back:", len(notfollowingback))

#### Get list of Friends to exclude (you want to continue to follow these)
listed = []
for page in tweepy.Cursor(api.list_members, list_owner, list_name, wait_on_rate_limit=True).pages():
    listed.extend(page)
exclude_list=[]
for one in listed:
    exclude_list.append(one.id)


print("Those in the list", str(list_name), "you do not want to unfollow:", len(exclude_list))


#### The drop list is are those who will be considered for your drop
drop = [x for x in notfollowingback if x not in exclude_list]
print("Those to drop:", len(drop))



epoch_time = int(time.time())
path = "backups/"+str(epoch_time)+str("_Unfollowed.txt")


def unfollow(a_user):
    print("Unfollowing %s" % a_user.screen_name)
    try:
        a_user.unfollow()
        with open(path,"a+") as file:
            file.write(str(a_user_id) + '\n')
    except Exception as e:
        er = e
        if e.api_code == 160:
            print("Request to befriend made, pending approval")
        if e.api_code == 50:
            print("User not found")
            pass
        else:
            print(e)
            try:
                time.sleep(10800) #3hrs
                a_user.unfollow()
                with open(path,"a+") as file:
                    file.write(str(a_user_id) + '\n')
            except:
                input("Tenacious error, press enter to skip user...")


for a_user_id in drop:
    a_user = api.get_user(a_user_id)
    if a_user.friends_count + a_user.followers_count < 6000: #### If user is not famous pass
        #print("Footprint is small", str(a_user.friends_count + a_user.followers_count))
        pass
    else: #### User is famous Unfollowing
        print("Footprint is large", str(a_user.friends_count + a_user.followers_count))
        if a_user.friends_count > 1.5*(a_user.followers_count):
            pass
        else:
            print("Does not follow others often", str(a_user.friends_count), "followed", str(a_user.followers_count))
            unfollow(a_user)
    time.sleep(1.1)


print("Completed")
Twitter_Tools.twitter_rates()


'''
for a_user_id in followers:
    a_user = api.get_user(a_user_id)
    print(a_user.friends_count, "https://twitter.com/"+a_user.screen_name)

2*(a_user.friends_count) > a_user.followers_count
a_user.friends_count + a_user.followers_count < 6000

'''
