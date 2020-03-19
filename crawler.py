import pymongo
from pymongo import MongoClient
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import time

client = pymongo.MongoClient('127.0.0.1',27017)
db = client.WebScience
db.WebScience.ensure_index("id", unique=True, dropDups=True)
collection = db.WebScience


class StdOutListener(StreamListener):

    def on_data(self, data):

        loadedtweet = json.loads(data)

        try:
            tweet_id = loadedtweet['id_str']  # tweet id
            username = loadedtweet['user']['screen_name']  # tweet author's username
            followers = loadedtweet['user']['followers_count']  # author's follower count
            text = loadedtweet['text']  # tweet body - note tweets over 140 characters will be truncated
            hashtags = loadedtweet['entities']['hashtags']  # hashtags in tweet
            dateTime = loadedtweet['created_at']  # when tweet was created

        # converting time tweet was created to easier format for mongoDB
            created = datetime.datetime.strptime(dateTime, '%a %b %d %H:%M:%S +0000 %Y')

            text = "" + text + ""

            tweet = {'id':tweet_id, 'username':username, 'followers':followers, 'text':text, 'hashtags':hashtags, 'created':created}

            collection.save(tweet)

            print (username + ':' + ' ' + text)
            return True
        except:
            print(loadedtweet)

    # Prints error of code 
    def on_error(self, status):
        print ("Error:" , status)

def rest_api(keywords,users_list):
    
    for user in users_list:
        try:
           for tweet in tweepy.Cursor(api.user_timeline, screen_name=user, exclude_replies = False, count = 10).items():
               text=tweet.text
               time=tweet.created_at
               username=tweet.user.screen_name
               print (username + ':' + ' ' + text)
        except tweepy.TweepError as e:
            print(e)

    for keyword in keywords:
        try:
           for tweet in tweepy.Cursor(api.search, q=keyword, lang="en").items():
               text=tweet.text
               time=tweet.created_at
               username=tweet.user.screen_name
               print (username + ':' + ' ' + text) 
        except tweepy.TweepError as e:
            print(e)

  
 ########## REPLACE BEFORE SUBMITTING!!!!!!!!!!!!!#####################   
consumer_key = "cyQtZjEeJ5TWl8jAl2UEbirLN"
consumer_secret = "O6kxD9M3m7kub9h6WIsgaXnWYKAOa2GGDCGqN6xW79jwEjmWs4"
access_token = "750813140326154240-W3ozr584bBPCzVUA2N8jYCnXK76pdd5"
access_token_secret = "QZroLr2y5YygdK2ZjQUievrJioZxEMzcE4CeoqJWj09ae"

keywords = ['coronavirus, COVID19, coronavirus uk']
users_list = ['realdonaldtrump', 'borisjohnston', 'bbcbreaking']
language = ['en']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Continuous stream of tweets
stream = Stream(auth, StdOutListener())
stream.filter(track=keywords, languages=language)

#Rest API
rest_api(keywords,users_list)

