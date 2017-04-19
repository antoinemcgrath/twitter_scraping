
A big thank you to https://github.com/bpb27 for the base/seed code https://github.com/bpb27/twitter_scraping  ####
MongoDB enhanced version at: https://github.com/antoinemcgrath/twitter_scraping

     This two step disjunction allows one to add tweets to your DB from a list of tweet ids that others have collected
     Likewise this method allows one to share lists of tweetids

twitter_DB_update_id_list.py
  Collect tweet ids & update mongo DB with collection progress

twitter_DB_update_tweets_metadata.py
  Query API with tweet ids & add json response to mongoDB

cron__twitter_DB_update_id_list.py
  Check first to see if the code is running before starting it (for cron starts)

python3 twitter_DB_update_tweets_metadata.py
  Retrieves tweet IDs from json files located in /mnt/8TB/GITS/twitter_scraping/tweet_ids/
  Adds them to mongoDB and deletes original files
python3 twitter_DB_update_id_list.py
  Compiles all tweet ids fetched from a users single day timeline & updates mongodb with the date completed
  Example of gnerated URL: https://twitter.com/search?f=tweets&vertical=default&q=from%3ABarackObama%20since%3A2016-03-14%20until%3A2016-03-15include%3Aretweets&src=typd

Possible ERRORS: After prolonged runs (~36hrs+) may start receiving twitter pages with no tweets.
         Activity is within twitter's robots.txt rate limit.
         (?) Potential browser error
         (?) Potential ISP/homerouter problem


