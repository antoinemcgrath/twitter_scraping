
A big thank you to https://github.com/bpb27 for the base/seed code https://github.com/bpb27/twitter_scraping  ####
MongoDB enhanced version at: https://github.com/antoinemcgrath/twitter_scraping

     This two step disjunction allows one to add tweets to your DB from a list of tweet ids that others have collected
     Likewise this method allows one to share lists of tweetids

twitter_DB_update_id_list.py
  Collect tweet id & update mongo DB with collection progress

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


Do not use any of the code I have written with harmful intent.

By using this code you accept that every person has the right to choose their own gender identity.


 Comments, critiques, need help? Contact me [![alt text][6.3]][3]  [![alt text][1.2]][1]

 <!-- Please don't remove this: Grab your social icons from https://github.com/carlsednaoui/gitsocial -->
 [1.2]: https://i.imgur.com/wWzX9uB.png (twitter icon without padding)
 [1]: https://www.twitter.com/AGreenDCBike
 [6.3]: http://i.imgur.com/9I6NRUm.png (github icon without padding)
 [3]: https://github.com/antoinemcgrath
