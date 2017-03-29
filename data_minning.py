from collections import defaultdict
import json
import operator
import validators
import json
import tweepy
#Adding your api key and secret here
api_key = '2hNqzcWDgUdZy4xBqhB5QZOW1'
api_secret = '7h83YOhKAhBSZDguPW1KLpcuzhCaE5q09qcXruweoKjYA6Qhtd'

#Adding your api token and secret here.
access_token = '834824567864582144-j64sQIlJPeVxRbHn7JRpuCFqyfGFiHO'
access_token_secret = 'Y1udhZoHNN7sKdkov221VoTDWieFpQr3VAgjFQQoe0gCF'

#Connecting twitter API
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

#Get the api
api = tweepy.API(auth)

#Function to catch urls from database.
def catch_url(input):
    frequency = defaultdict(int)
    for tweet in tweepy.Cursor(api.search, q=input, rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(100):
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
                               rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(100):
        temp = tweet.entities.get("hashtags")
        if temp is not None:
            for item in temp:
                if item is not None:
                    frequency_hash[item.get('text')] += 1
    sorted_x = sorted(frequency_hash.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_x

a="http://www.foxnews.com/politics/2017/03/27/sessions-takes-aim-at-dangerous-sanctuary-cities-warns-on-funding.html"
used_url=set()
map={}
map[a]={}
used_url.add(a)
hashtag=catch_hashtags(a)
for x in range(len(hashtag)):
    if hashtag[x][0] not in map[a] and x<5:
        map[a]["#"+hashtag[x][0]]=set()
for key in map[a].keys():
    url=catch_url(key)
    for i in range(len(url)):
        if url[i][0] not in map and i<5:
            map[url[i][0]]={}
            map[a][key].add(url[i][0])
for key in map.keys():
    if key not in used_url:
        hashtag=catch_hashtags(key)
        for j in range(len(hashtag)):
            if hashtag[j][0] not in map[key] and j < 5:
                map[key][hashtag[j][0]]=set()
for key_url in map.keys():
    if key_url not in used_url:
        for key_hashtag in map[key_url].keys():
            url = catch_url(key_hashtag)
            for i in range(len(url)):
                if i<5:
                    map[key_url][key_hashtag].add(url[i][0])
print(map)