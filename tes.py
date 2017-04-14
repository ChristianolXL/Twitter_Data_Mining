#Tianxin Zhou and Weike Dai
#Last edited 04/06/2017

from collections import defaultdict
import json
import operator
import time
import json
import tweepy
import numpy as np
#Adding your api key and secret here
api_key = 'Z7XrZPn7hJxclnfcdkJY5itbJ'
api_secret = '4SMhwdNNMupw6QisSVPHnHwbTUR66iqYANaTuCkDOfx15KSggC'

#Adding your api token and secret here.
access_token = '2745445122-tCYm5SOst4Xr72xDC2nyuswytF0o8cLWTWAZMuD'
access_token_secret = 'RkKMWZ1psNYzQE4QdvjwxXWbach8QG7LIxJegjw8Oiyjh'

#Connecting twitter API
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

#Get the api
api = tweepy.API(auth)

#Function to catch urls from database.
def catch_url(input):
    print("The key argument that we want to catch")
    print(input)
    print("The time stamp for the tweets:")
    frequency = defaultdict(int)
    count1 = 0
    for tweet in tweepy.Cursor(api.search, q=input, rpp=100, count=100, result_type="recent", include_entities=True, lang="en").items(1000):
        temp = tweet.entities.get("urls")
        print (tweet.created_at)
        count1 = count1 + 1
        for item in temp:
            frequency[item.get('url')]+=1

    print(count1)
    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)
    print (sorted_x)
    return sorted_x

#Function to catch hashtags from database.
def catch_hashtags(input):
    frequency_hash = defaultdict(int)
    for tweet in tweepy.Cursor(api.search,
                               q=input,
                               rpp=100, count=100, result_type="recent", include_entities=True, lang="en").items(100):
        temp = tweet.entities.get("hashtags")
        if temp is not None:
            for item in temp:
                if item is not None:
                    frequency_hash[item.get('text')] += 1

    sorted_x = sorted(frequency_hash.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_x

#Will add comments later
#The original node.
a="http://www.spin.com/2017/04/kendrick-lamar-new-album-april-14-itunes/"

catch_url("AI")