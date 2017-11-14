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







#### Define twitter rate determining loop
#Follow add rate limited to 1000 per 24hrs: https://support.twitter.com/articles/15364
def twitter_rates():
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
twitter_rates()



friends = api.friends_ids(api.me().id)
followers = api.followers_ids(api.me().id)
print("Starting: Friend count:",len(friends))
print("Starting: Follower count:",len(followers))

notfollowingback = [x for x in friends if x not in followers]
print("Starting: Not following back:", len(notfollowingback))


for a_user_id in notfollowingback:
    a_user = api.get_user(a_user_id)
    print("Unfollowing %s" % a_user.screen_name)
    try:
        a_user.unfollow()
    #except:
    #    print("  .. failed, sleeping for 5 seconds and then trying again.")
    except tweepy.error.TweepError as e:
        twitter_rates()
        print (e.reason)
        time.sleep(10800) #3hrs
        a_user.unfollow()
    #print(" .. completed, sleeping for 1 second.")
    time.sleep(1)


print("Completed")
twitter_rates()


print("Starting: Friend count:",len(friends))
print("Starting: Follower count:",len(followers))
print("Starting: Not following back:", len(notfollowingback))


friends = api.friends_ids(api.me().id)
followers = api.followers_ids(api.me().id)
print("New: Friend count:",len(friends))
print("New: Follower count:",len(followers))

notfollowingback = [x for x in friends if x not in followers]
print("New: Not following back:", len(notfollowingback))


#### To print the number of users a person follows (aid for detecting bots and commerical opperations)
'''
friends = api.friends(api.me().id)
followers = api.followers_ids(api.me().id)
len(followers)
foll = []
for a_user_id in followers:
    a_user = api.get_user(a_user_id)
    foll.append(a_user)

for a_user_id in followers:
    a_user = api.get_user(a_user_id)
    print(a_user.friends_count, "https://twitter.com/"+a_user.screen_name)
'''
