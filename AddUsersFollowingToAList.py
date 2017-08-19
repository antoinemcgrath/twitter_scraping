#### A script for copying the twitter users you follow into one of your twitter lists

#### Specify your destination list
list = 'leaders'


import json
import tweepy
import time
import re

#### Load API keys file
keys_json = json.load(open('/usr/local/keys.json'))

#### Specify key dictionary wanted (generally [Platform][User][API])
#Keys = keys_json["Twitter"]["ClimateCong_Bot"]["ClimatePolitics"]
Keys = keys_json["Twitter"]["AGreenDCBike"]["HearHerVoice"]

#### Access API using key dictionary definitions
auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth)
user = Keys['Owner']







#### Define Twitter API rates determining loop
#Follow add rate limited to 1000 per 24hrs: https://support.twitter.com/articles/15364
def twitter_API_rates():
    rate_limits = api.rate_limit_status()['resources']
    new = str(rate_limits).split("'/")
    for anew in new[1:]: #skip the first one item it is not a limit key
        limit_value = (anew.split("':"))[0]
        anew_json = (anew[anew.find("{"):anew.find("}")+1]).replace("'",'"')
        vals = json.loads(anew_json)
        c = vals['limit']
        #d = vals['reset']
        e = vals['remaining']
        f = c-e
        if f != 0:
            #print(anew)
            print("Used:" + str(f) + "  Remaining:" + str(e) + "  " + limit_value)
        else:
            pass


twitter_API_rates()


#### Get the list of users
#followers = api.followers_ids(user)
list1 = friends = api.friends_ids(user)
print("The number of users followed is: " +str(len(list1)))


#### Get list of user ids from those within the list of interest
listed = []
for page in tweepy.Cursor(api.list_members, user, list).pages():
    listed.extend(page)
    #time.sleep(2)
    #twitter_API_rates()
    #print(len(listed))

list2=[]
for one in listed:
    list2.append(one.id)

print("The number of users in the destination list is: " +str(len(list2)))


#### Remove those user ids which are already in the list
list3 = []
list3 =  [x for x in list1 if x not in list2]


print("The number of users to be transfered to the desitination list is: " +str(len(list3)))

#### Stop script if there are no users to add to the destination
if list3 == []:
    twitter_API_rates()
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
    api.add_list_member(user_id=one, slug=list, owner_screen_name=user)
    #print(one)
    time.sleep(6) #6secs
    index += 1
    print(index)
    if max_index < index:
      break
  except tweepy.error.TweepError as e:
    twitter_API_rates()
    print (e.reason)
    time.sleep(10800) #3hrs



print("Completed")
twitter_API_rates()