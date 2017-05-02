#Tianxin Zhou and Weike Dai
#Last updated 04/26/2017
#This programing is going to use one url as the mother node to find other urls that relates to it.

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
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Record the speak that have most retweet count for every url.
speakmap={}

#Creat the file to store time and frequency stats
f = open("Frequency_table","w")

#Function to catch urls from database.
def catch_url(input):
    print("The key argument that we want to catch",file=f)
    print(input,file=f)
    print("The time stamp for the tweets:",file=f)
    frequency = defaultdict(int)
    for tweet in tweepy.Cursor(api.search, q=input, rpp=100, count=100, result_type="recent", include_entities=True, lang="en").items(1000):
        temp = tweet.entities.get("urls")
        print(tweet.created_at,file=f)
        for item in temp:
            frequency[item.get('url')]+=1

    print("The frequency table: ",file=f)

    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)
    print(sorted_x, file=f)
    return sorted_x

#Function to catch hashtags from database.
def catch_hashtags(input):
    print("The key argument that we want to catch",file=f)
    print(input,file=f)
    print("The time stamp for the tweets:",file=f)
    frequency_hash = defaultdict(int)
    rtcount = 0
    maxtweet = ""
    for tweet in tweepy.Cursor(api.search,
                               q=input,
                               rpp=100, count=100, result_type="recent", include_entities=True, lang="en").items(1000):
        temp = tweet.entities.get("hashtags")

        #Find the most popular text
        if(tweet.retweet_count > rtcount):
            maxtweet = tweet.text
        print(tweet.created_at, file=f)
        if temp is not None:
            for item in temp:
                if item is not None:

                    #Add the hashtag into frequency dict and change the hashtag to lowercase.
                    frequency_hash[item.get('text').lower()] += 1
    print("The frequency table: ",file=f)
    speakmap[input] = maxtweet

    sorted_x = sorted(frequency_hash.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_x, file=f)
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
next_url = set()
next_url2 = set()

#The limitation is 150 requests per 15min.
#The first loop to get hashtags from the mother node.
for x in range(len(hashtag)):
    if hashtag[x][0] not in map[a] and x<(0.1*len(hashtag)):
        map[a]["#"+hashtag[x][0]]=set()

#The First loop to get the urls by hashtags of mother node.
for key in map[a].keys():
    url=catch_url(key)
    count = + 1
    for i in range(len(url)):
        if url[i][0] not in map and i<(5):
            map[url[i][0]]={}
            map[a][key].add(url[i][0])

#The second loop to get hashtags from child nodes.
for key in map.keys():
    if key not in used_url:
        hashtag=catch_hashtags(key)
        count =+ 1
        for j in range(len(hashtag)):
            if hashtag[j][0] not in map[key] and j < (0.1*len(hashtag)):
                map[key]["#"+hashtag[j][0]]=set()


#The second loop to get urls by hashtags of child nodes.
for key_url in map.keys():
    if key_url not in used_url:
        for key_hashtag in map[key_url].keys():
            url = catch_url(key_hashtag)
            count =+ 1
            for i in range(len(url)):
                if i<(5):
                    map[key_url][key_hashtag].add(url[i][0])
                    next_url.add(url[i][0])

#Add url to the dict.
for url in next_url:
    if url not in map:
        map[url] = {}

#Find the hashtags of new urls.
for key in next_url:
    hashtag = catch_hashtags(key)
    count = + 1
    for j in range(len(hashtag)):
        if hashtag[j][0] not in map[key] and j < 2:
            map[key]["#"+hashtag[j][0]] = set()

#Find the urls by the new hashtags.
for key_url in next_url:
    for key_hashtag in map[key_url].keys():
        url = catch_url(key_hashtag)
        count = + 1
        for i in range(len(url)):
            if i < 5:
                map[key_url][key_hashtag].add(url[i][0])


#save
#map stores the dict of {url, {hashtag, (urls)}}
np.save('my_file.npy', map)

#speakmap stores the dict of {url, content}
np.save('speak_file.npy', speakmap)
print (count)
f.close()