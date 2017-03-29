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
        print(tweet.text, tweet.entities.get("hashtags"))
        temp = tweet.entities.get("hashtags")
        if temp is not None:
            for item in temp:
                if item is not None:
                    frequency_hash[item.get('text')] += 1
    sorted_x = sorted(frequency_hash.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_x


#Testing catch_url.
sorted_x = catch_url("http://www.theverge.com/2017/3/27/15077864/elon-musk-neuralink-brain-computer-interface-ai-cyborgs")
file =open("urls.txt","w")
for x in range(len(sorted_x)):
    file.write(str(sorted_x[x][0]))
    file.write("["+str(sorted_x[x][1])+"]")
    file.write("\n")


#Testing catch_hashtags.
sorted_x = catch_hashtags("http://www.theverge.com/2017/3/27/15077864/elon-musk-neuralink-brain-computer-interface-ai-cyborgs")
file=open("hashtag.txt","w")
for x in range(len(sorted_x)):
    file.write(str(sorted_x[x][0]))
    file.write("["+str(sorted_x[x][1])+"]")
    file.write("\n")