#!/usr/bin/python3

###################################################################
#  Do not use any of the code I have written with harmful intent. #
#                                                                 #
#    By using this code you accept that everyone has the          #
#       right to choose their own gender identity.                #
###################################################################

import json
import math
from pymongo import MongoClient
import datetime
connection = c = MongoClient()
db = connection.Twitter
#db.tweets.create_index("id", unique=True, dropDups=True)
db.politicians.ensure_index( "id", unique=True, dropDups=True )
collection = db.politicians



##Similar direct in mongo## db.politicians_test.find().forEach(function(doc){doc.created_at = new Date(doc.created_at);db.politicians_test.save(doc)})
from bson.objectid import ObjectId
not_UNIXtimed = db.politicians.find({ "created_at": {'$exists': True}, "user.created_at": {'$exists': True}, "created_at_UNIXtime": {'$exists': False}})
not_UNIXtimed.count()
for one_item in not_UNIXtimed:
    one_created_at_UNIXtime = (int(datetime.datetime.strptime(one_item['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%s")))
    one_usercreated_at_UNIXtime = (int(datetime.datetime.strptime(one_item['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%s")))
    one_id = (str(one_item['_id']))
    print (one_id +" "+ str(one_created_at_UNIXtime) +" "+ str(one_usercreated_at_UNIXtime))
    db.politicians.update_one({'_id': ObjectId(one_id)}, {'$set': {'created_at_UNIXtime': one_created_at_UNIXtime, 'user.created_at_UNIXtime': one_usercreated_at_UNIXtime}})
