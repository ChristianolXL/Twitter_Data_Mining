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
    frequency = defaultdict(int)
    for tweet in tweepy.Cursor(api.search, q=input, rpp=100, count=100, result_type="recent", include_entities=True, lang="en").items(100):
        temp = tweet.entities.get("urls")
        for item in temp:
            frequency[item.get('url')]+=1
    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)
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
a="http://www.theverge.com/2017/3/27/15077864/elon-musk-neuralink-brain-computer-interface-ai-cyborgs"
used_url=set()
map={}
map[a]={}
used_url.add(a)
hashtag=catch_hashtags(a)
count = 1
#The limitation is 150 requests per 15min.
for x in range(len(hashtag)):
    if hashtag[x][0] not in map[a] and x<5:
        map[a]["#"+hashtag[x][0]]=set()
for key in map[a].keys():
    url=catch_url(key)
    count = + 1
    if (count / 150 == 0):
        print("Limitation reached")
        time.sleep(60 * 15)
    for i in range(len(url)):
        if url[i][0] not in map and i<5:
            map[url[i][0]]={}
            map[a][key].add(url[i][0])
for key in map.keys():
    if key not in used_url:
        hashtag=catch_hashtags(key)
        count =+ 1
        if(count/150 == 0):
            print ("Limitation reached")
            time.sleep(60*15)

        for j in range(len(hashtag)):
            if hashtag[j][0] not in map[key] and j < 2:
                map[key]["#"+hashtag[j][0]]=set()
for key_url in map.keys():
    if key_url not in used_url:
        for key_hashtag in map[key_url].keys():
            url = catch_url(key_hashtag)
            count =+ 1
            if (count / 150 == 0):
                print("Limitation reached")
                time.sleep(60 * 15)
            for i in range(len(url)):
                if i<5:
                    map[key_url][key_hashtag].add(url[i][0])

#save
np.save('my_file.npy', map)

print (count)
