# Twitter Data Mining


## Getting Started

  #Thie# project includes two programs, one called Datadownload which will download the data from twitter as NPY format, and another called Translator which will translate the data from NPY format into XML format.<br />
  The algorithm to collecting data: <br />
  Use the url you insterested in as the mother node, then requests 1000 tweets that contain the url and stores every hashtag in those tweets into a dictionary with the frequency of the hashtag.<br />
  Request 1000 tweets for every hashtag wich has top 10% frequency in the dictionary and store every url appears in the tweets with its frequency. Then choose the urls with top 10% frequency for each hashtags, add them to the database as other nodes with the hashtag as the relationship.<br />
  Then use the new node to collect hashtags and so on..<br />

### Prerequisites

What things you need to install the software and how to install them

Python version 3.X 
<br />

Modules:<br />
Tweepy<br />
Numpy<br />
lxml<br />

### Installing

A step by step series of examples that tell you have to get a development env running
<br />
Say what the step will be
<br />
Modules installing example:<br />
pip3 install tweepy<br />
pip3 install numpy<br />
pip3 install lxml<br />


## Running the tests

  First of all, you should create a twitter on (https://apps.twitter.com), and copy the api key/secret and api token/secret to the variables in the Datadownload. If you don't like to create one, feel free to use the default api key and secret. <br />
  Second, change the variables as you want:<br />
    Dictname: the name of .npy file stores the url and hashtags. <br />
    SpeakDictname: the name of .npy file stores content of the speak content. <br />
    Frequency_table: the name of .txt file stores the frequency of hashtags/ urls.<br />
    mother_node: the First url we want to expand.<br />
    Num_level: the number of node level you want, the maximum number is 4, since for 3 levels the program needs hours to get        the result due to the twitter api limitation, so currently The program only supports 4 level of nodes.<br />
  Third, 
  


## Authors

 **Tianxin Zhou/ Weike Dai** 


