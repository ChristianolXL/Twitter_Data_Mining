from collections import defaultdict
import json
import operator
import validators
import json
import tweepy
api_key = '2hNqzcWDgUdZy4xBqhB5QZOW1'
api_secret = '7h83YOhKAhBSZDguPW1KLpcuzhCaE5q09qcXruweoKjYA6Qhtd'

access_token = '834824567864582144-j64sQIlJPeVxRbHn7JRpuCFqyfGFiHO'
access_token_secret = 'Y1udhZoHNN7sKdkov221VoTDWieFpQr3VAgjFQQoe0gCF'



auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

frequency = defaultdict(int)
for tweet in tweepy.Cursor(api.search, q="http://www.foxnews.com/politics/2017/03/27/sessions-takes-aim-at-dangerous-sanctuary-cities-warns-on-funding.html", rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(100):
   temp = tweet.entities.get("urls")
   for item in temp:
       frequency[item.get('url')]+=1

sorted_x = sorted(frequency.items(), key=operator.itemgetter(1),reverse=True)





file =open("urls.txt","w")
for x in range(len(sorted_x)):
    file.write(str(sorted_x[x][0]))
    file.write("["+str(sorted_x[x][1])+"]")
    file.write("\n")




frequency_hash = defaultdict(int)
for tweet in tweepy.Cursor(api.search, q="#google", rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(10):
   temp = tweet.entities.get("hashtags")
   
   if temp is not None:
    for item in temp:
       if item is not None:
        frequency_hash[item.get('text')]+=1


sorted_x = sorted(frequency_hash.items(), key=operator.itemgetter(1),reverse=True)


file=open("hashtag.txt","w")
for x in range(len(sorted_x)):
    file.write(str(sorted_x[x][0]))
    file.write("["+str(sorted_x[x][1])+"]")
    file.write("\n")