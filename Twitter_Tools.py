import json

def get_api_keys():
    #### Set Twitter API key dictionary
    try:    #### Attempt to load API keys file
        keys_json = json.load(open('/usr/local/keys.json'))
        #### Specify key dictionary wanted (generally [Platform][User][API])
        #Keys = keys_json["Twitter"]["ClimateCong_Bot"]["ClimatePolitics"]
        Keys = keys_json["Twitter"]["AGreenDCBike"]["HearHerVoice"]
    except Exception as e:
        er = e
        if er.errno == 2: #File not found enter key dictionary values manually
            print("\nNo twitter API key was found in /usr/local/keys.json\n",
                 "Acquire an API key at https://apps.twitter.com/\n",
                 "to supply key manually press Enter\n")
            Keys = {}
            Keys['Consumer Key (API Key)'] = input('Enter the Twitter API Consumer Key\n')
            Keys['Consumer Secret (API Secret)'] = input('Enter the Twitter API Consumer Secret Key\n')
            Keys['Access Token'] = input('Enter the Twitter API Access Token\n')
            Keys['Access Token Secret'] = input('Enter the Twitter API Access Token Secret\n')
            Keys['Owner'] = input('Enter your Twitter username associated with the API keys\n')
        else:
            print(e)
    return(Keys)
