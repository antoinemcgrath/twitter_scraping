

gen_time = int(datetime.datetime.strptime("Mon Jul 03 02:37:16 +0000 2017",'%a %b %d %H:%M:%S +0000 %Y').strftime("%s"))
result = db.politicians.find({ "created_at_UNIXtime": { "$gt": gen_time }, "user.screen_name": users_re, "text": keywords_re})

BEST

from bson.objectid import ObjectId
not_UNIXtimed = db.politicians.find({ "created_at": {'$exists': True}, "user.created_at": {'$exists': True}, "created_at_UNIXtime": {'$exists': False}})
not_UNIXtimed.count()
for one_item in not_UNIXtimed:
    one_created_at_UNIXtime = (int(datetime.datetime.strptime(one_item['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%s")))
    one_usercreated_at_UNIXtime = (int(datetime.datetime.strptime(one_item['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y').strftime("%s")))
    one_id = (str(one_item['_id']))
    print (one_id +" "+ str(one_created_at_UNIXtime) +" "+ str(one_usercreated_at_UNIXtime))
    db.politicians.update_one({'_id': ObjectId(one_id)}, {'$set': {'created_at_UNIXtime': one_created_at_UNIXtime, 'user.created_at_UNIXtime': one_usercreated_at_UNIXtime}})
