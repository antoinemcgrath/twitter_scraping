# Rapid twitter viewer


count = 0
try:
    #API.list_timeline(owner, slug[, since_id][, max_id][, per_page][, page])
    twrecents = api.list_timeline(owner_screen_name=twitter_user, slug=tw_list_id, count=150)
    for tweet in twrecents:
        count = count + 1
        print (count)
        print (id_str, tweet.created_at, tweet.text)
    #api.get_list(slug=tw_list_id, owner_screen_name=twitter_user)
except tweepy.error.TweepError as e:
    print ("Tweepy Error")
    print (e)



# General Stream Search # for tweet in tweepy.Cursor(api.search, q="google", rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(200):
# List search #
for tweet in tweepy.Cursor(api.list_timeline, q="google", owner_screen_name=twitter_user, slug=tw_list_id, rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(200):
    print (tweet.created_at, tweet.text)
