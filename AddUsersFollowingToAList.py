#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

#### A script for copying the twitter users you follow into one of your twitter lists

#### Specify your destination list
lists = ['leaders','leaders2']

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



#### Get the list of users
#followers = api.followers_ids(user)
list1 = friends = api.friends_ids(user)
print("The number of users followed is: " +str(len(list1)))


#### Get list of user ids from those within the list of interest
listed = []
for a_list in lists:
    for page in tweepy.Cursor(api.list_members, user, a_list, wait_on_rate_limit=True).pages():
        listed.extend(page)
        #time.sleep(2)
        #print(len(listed))

list2=[]
for one in listed:
    list2.append(one.id)

print("The number of users in the destination list", list, "is: ", str(len(list2)))


#### Remove those user ids which are already in the list
list3 = []
list3 =  [x for x in list1 if x not in list2]


print("The number of users to be transfered to the desitination list is: " +str(len(list3)))

#### Stop script if there are no users to add to the destination
if list3 == []:
    Twitter_Tools.twitter_rates(api)
    print("All users in destination list already.")
    exit()
else:
    pass

#### Add each user in list3 to the list, print twitter API rates and sleep if errors occur
index = 0
max_index = len(list3)-1
print(max_index)
while True:
  one = list3[index]
  try:
    api.add_list_member(user_id=one, slug=lists[1], owner_screen_name=user)
    #print(one)
    time.sleep(15) #6secs
    index += 1
    print(index)
    if max_index < index:
      break
  except tweepy.error.TweepError as e:
    Twitter_Tools.twitter_rates(api)
    print (e.reason)
    time.sleep(10800) #3hrs



print("Completed")
Twitter_Tools.twitter_rates(api)
