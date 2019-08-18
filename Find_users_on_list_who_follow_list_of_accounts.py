#!/usr/bin/python3

###################################################################
#  Please do not use any code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

####
#### Specify a list of respected Twitter handles and see how
####    many of them follow accounts in a list

#### Specify your list of trusted users
list = 'leaders'
#### Specify your list of accounts 
compares = 'nm-private-list'
print(list)
print(compares)
import sys
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
list_owner = Keys['Owner']


#### Get list of user ids from those within the list of interest
respected_users = []
for page in tweepy.Cursor(api.list_members, list_owner, list, wait_on_rate_limit=True).pages():
    respected_users.extend(page)
    #time.sleep(2)


res_users = []
for respected in respected_users:
    res_users.append(respected.id)


print("The number of respected_users is: ", str(len(res_users)))


list_of_compares = []
for page in tweepy.Cursor(api.list_members, list_owner, compares, wait_on_rate_limit=True).pages():
    list_of_compares.extend(page)


print("The number of accounts to compare to is " + str(len(list_of_compares)))



#### User less important handle to access bulk of the data
keys_json = json.load(open('/usr/local/keys.json'))
#Keys = keys_json["Twitter"]["ClimateCong_Bot"]["ClimatePolitics"]
Keys = keys_json["Twitter"]["ClimateCong_Bot"]["Python_ClimateCongressBot"]

auth = tweepy.OAuthHandler( Keys['Consumer Key (API Key)'], Keys['Consumer Secret (API Secret)'] )
auth.set_access_token( Keys['Access Token'], Keys['Access Token Secret'] )
api = tweepy.API(auth, wait_on_rate_limit=True)
Twitter_Tools.twitter_rates(api)


def get_followers(user_id):
    users = []
    page_count = 0
    for i, user in enumerate(tweepy.Cursor(api.followers_ids, id=user_id, count=5000).pages()):
        print ('Getting page {} for followers'.format(i))
        users += user
        #print(users)
        time.sleep(2)
    return users




for one_account in list_of_compares:
    print(str(one_account.screen_name) + " followers count is " + str(one_account.followers_count))
    contin = Twitter_Tools.query_yes_no(str("Include this user? " + str(one_account.screen_name)))
    if contin == True:
        follow_list = get_followers((str(one_account.screen_name)))
        print((str(one_account.screen_name)) + " follower count is " + str(len(follow_list))
            + " has " +
            str(len(set(follow_list) & set(res_users)))
            + " respected followers")
        #Twitter_Tools.twitter_rates(api)
        time.sleep(3)
    else:
        pass


#### To remove the first item in the list once results have been given
##list_of_compares[0].screen_name
##del list_of_compares[0]
##len(list_of_compares)