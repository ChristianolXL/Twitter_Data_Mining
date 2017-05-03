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
#If need, please change the following variables as you like.
#Adding your api key and secret here
api_key = 'Z7XrZPn7hJxclnfcdkJY5itbJ'
api_secret = '4SMhwdNNMupw6QisSVPHnHwbTUR66iqYANaTuCkDOfx15KSggC'

#Adding your api token and secret here.
access_token = '2745445122-tCYm5SOst4Xr72xDC2nyuswytF0o8cLWTWAZMuD'
access_token_secret = 'RkKMWZ1psNYzQE4QdvjwxXWbach8QG7LIxJegjw8Oiyjh'

#Variables setting
#Dictname: the name of .npy file stores the url and hashtags.
#SpeakDictname: the name of .npy file stores content of the speak content.
#Frequency_table: the name of .txt file stores the frequency of hashtags/ urls.
#mother_node: the First url we want to expand.
#Num_level: the number of node level you want, the maximum number is 4, since for 3 levels the program needs hours to get the result due to the twitter api limitation, so currently The program only supports 4 level of nodes.
#num: the percentage of top frequency item you want, the default is 0.1.

Dictname = 'Example_dict'
SpeakDictname = "Example_speak.npy"
Frequency_table = "Example_Frequency_table.txt"
mother_node="http://www.theverge.com/2017/3/27/15077864/elon-musk-neuralink-brain-computer-interface-ai-cyborgs"
toprate_hashtags = 0.5
toprate = 0.02
num = 2

#Connecting twitter API
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

#Get the api
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#Record the speak that have most retweet count for every url.
speakmap={}

#Creat the file to store time and frequency stats
f = open(Frequency_table,"w")

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
def download(num):
    used_url=set()
    map={}
    map[mother_node]={}
    used_url.add(mother_node)
    hashtag=catch_hashtags(mother_node)
    next_url = set()

    #The limitation is 150 requests per 15min.
    #The first loop to get hashtags from the mother node.
    for x in range(len(hashtag)):
        if hashtag[x][0] not in map[mother_node] and x<(toprate_hashtags*len(hashtag)):
            map[mother_node]["#"+hashtag[x][0]]=set()

    #The First loop to get the urls by hashtags of mother node.
    for key in map[mother_node].keys():
        url=catch_url(key)
        for i in range(len(url)):
            if url[i][0] not in map and i<(toprate*len(url)):
                map[url[i][0]]={}
                map[mother_node][key].add(url[i][0])

    if(num < 2):
        return map


    #The second loop to get hashtags from child nodes.
    for key in map.keys():
        if key not in used_url:
            hashtag=catch_hashtags(key)
            for j in range(len(hashtag)):
                if hashtag[j][0] not in map[key] and j < (toprate_hashtags*len(hashtag)):
                    map[key]["#"+hashtag[j][0]]=set()
    
    
    #The second loop to get urls by hashtags of child nodes.
    for key_url in map.keys():
        if key_url not in used_url:
            for key_hashtag in map[key_url].keys():
                url = catch_url(key_hashtag)
                for i in range(len(url)):
                    if i<((toprate*len(url))):
                        map[key_url][key_hashtag].add(url[i][0])
                        next_url.add(url[i][0])
    
    if(num < 3):
        return map

    #The third level.
    #Add url to the dict.
    for url in next_url:
        if url not in map:
            map[url] = {}
        else:
            next_url.remove(url)
    
    #Find the hashtags of new urls.
    for key in next_url:
        hashtag = catch_hashtags(key)
        for j in range(len(hashtag)):
            if hashtag[j][0] not in map[key] and j < (toprate_hashtags*len(hashtag)):
                map[key]["#"+hashtag[j][0]] = set()
    new_url = set()
    #Find the urls by the new hashtags.
    for key_url in next_url:
        for key_hashtag in map[key_url].keys():
            url = catch_url(key_hashtag)
            for i in range(len(url)):
                if i < (toprate*len(url)):
                    map[key_url][key_hashtag].add(url[i][0])
                    new_url.add(url[i][0])
    if (num < 4):
        return map
    # The forth level.
    # Add url to the dict.
    for url in new_url:
        if url not in map:
            map[url] = {}
        else:
            new_url.remove(url)

    # Find the hashtags of new urls.
    for key in new_url:
        hashtag = catch_hashtags(key)
        for j in range(len(hashtag)):
            if hashtag[j][0] not in map[key] and j < (toprate_hashtags * len(hashtag)):
                map[key]["#" + hashtag[j][0]] = set()
    # Find the urls by the new hashtags.
    for key_url in new_url:
        for key_hashtag in map[key_url].keys():
            url = catch_url(key_hashtag)
            for i in range(len(url)):
                if i < (toprate * len(url)):
                    map[key_url][key_hashtag].add(url[i][0])
    return map

def main():

    result = download(num)
    # save
    # map stores the dict of {url, {hashtag, (urls)}}
    np.save(Dictname, result)

    # speakmap stores the dict of {url, content}
    np.save(SpeakDictname, speakmap)

    f.close()

if __name__ == "__main__":
    main()

