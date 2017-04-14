for key in map.keys():
    if key not in used_url:
        hashtag=catch_hashtags(key)
        count = count + 1
        if(count%150 == 0):
            print ("Limitation reached")
            time.sleep(60*15)

        for j in range(len(hashtag)):
            if hashtag[j][0] not in map[key] and j < 2:
                map[key][hashtag[j][0]]=set()



#Adding your api key and secret here
api_key = 'Z7XrZPn7hJxclnfcdkJY5itbJ'
api_secret = '4SMhwdNNMupw6QisSVPHnHwbTUR66iqYANaTuCkDOfx15KSggC'

#Adding your api token and secret here.
access_token = '2745445122-tCYm5SOst4Xr72xDC2nyuswytF0o8cLWTWAZMuD'
access_token_secret = 'RkKMWZ1psNYzQE4QdvjwxXWbach8QG7LIxJegjw8Oiyjh'


for key_url in map.keys():
    if key_url not in used_url:
        for key_hashtag in map[key_url].keys():
            url = catch_url(key_hashtag)
            count =+ 1
            for i in range(len(url)):
                if i<5:
                    map[key_url][key_hashtag].add(url[i][0])
                    next_url.add(url[i][0])