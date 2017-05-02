# Twitter Data Mining


## Getting Started

  Thie project includes two programs, one called Datadownload which will download the data from twitter as NPY format, and another called Translator which will translate the data from NPY format into XML format.
  The algorithm to collecting data: 
    Use the url you insterested in as the mother node, then requests 1000 tweets that contain the url and stores every hashtag in those tweets into a dictionary with the frequency of the hashtag.
    Request 1000 tweets for every hashtag wich has top 10% frequency in the dictionary and store every url appears in the tweets with its frequency. Then choose the urls with top 10% frequency for each hashtags, add them to the database as other nodes with the hashtag as the relationship.
    Then use the new node to collect hashtags and so on..

### Prerequisites

What things you need to install the software and how to install them

Python version 3.X 

Modules:
Tweepy
Numpy
lxml

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

Modules installing example:
pip3 install tweepy
pip3 install numpy
pip3 install lxml


## Running the tests

  First of all, you should create a twitter on (https://apps.twitter.com), and copy the api key/secret and api token/secret to the variables in the Datadownload. If you don't like to create one, feel free to use the default api key and secret. 
  Second, change the variables as you want:
    Dictname: the name of .npy file stores the url and hashtags. 
    SpeakDictname: the name of .npy file stores content of the speak content. 
    Frequency_table: the name of .txt file stores the frequency of hashtags/ urls.
    mother_node: the First url we want to expand.
    Num_level: the number of node level you want, the maximum number is 4, since for 3 levels the program needs hours to get        the result due to the twitter api limitation, so currently The program only supports 4 level of nodes.
  Third, 
  


## Authors

 **Tianxin Zhou/ Weike Dai** 


