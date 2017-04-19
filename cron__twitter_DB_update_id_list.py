#!/usr/bin/python3

#script = "/mnt/8TB/GITS/twitter_scraping/cron__twitter_DB_update_id_list.py"

#Execution schedule is everyday at 2:30AM and PM  ##crontab -e
##30 2 * * * /usr/bin/python3 /mnt/8TB/GITS/twitter_scraping/cron__twitter_DB_update_id_list.py
##30 14 * * * /usr/bin/python3 /mnt/8TB/GITS/twitter_scraping/cron__twitter_DB_update_id_list.py



import subprocess
processor = "python3"
script = "/mnt/8TB/GITS/twitter_scraping/twitter_DB_update_id_list.py"


processing = subprocess.Popen(['ps', '-O', '.py'], stdout=subprocess.PIPE).communicate()
print (processing)
if (str(processing).find(script) > 0) == False:
    print("False: Script " + script + " is not running.")
    subprocess.Popen([processor, script])
else:
    print("True: Script " + script + " is running.")
    
