import pymongo
from pymongo import MongoClient
import json
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import time
from credentials import *

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client.WebScience
db.WebScience.create_index("id", unique=True, dropDups=True)
collection = db.WebScience


class StdOutListener(StreamListener):

    def on_data(self, data):

        loadedtweet = json.loads(data)

        try:
            tweet_id = loadedtweet['id_str']  # tweet id
            # tweet author's username
            username = loadedtweet['user']['screen_name']
            # author's follower count
            followers = loadedtweet['user']['followers_count']
            # tweet body - note tweets over 140 characters will be truncated
            text = loadedtweet['text']
            hashtags = loadedtweet['entities']['hashtags']  # hashtags in tweet
            dateTime = loadedtweet['created_at']  # when tweet was created

        # converting time tweet was created to easier format for mongoDB
            created = datetime.datetime.strptime(
                dateTime, '%a %b %d %H:%M:%S +0000 %Y')

            text = "" + text + ""

            tweet = {'id': tweet_id, 'username': username, 'followers': followers,
                     'text': text, 'hashtags': hashtags, 'created': created}

            collection.insert_one(tweet)

            print(username + ':' + ' ' + text)
            return True
        except:
            print(loadedtweet)
         
            

    # Prints error of code
    def on_error(self, status):
        print("Error:", status)


def rest_api(keywords, users_list):

    for user in users_list:
        try: # prints tweets from user's timeline
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=user, exclude_replies=False, count=10).items():
                text = tweet.text
                time = tweet.created_at
                username = tweet.user.screen_name
                print(username + ':' + ' ' + text + ' ' + time)
        except tweepy.TweepError as e:
            print("Error: ", e)

    for keyword in keywords:
        try: # prints tweets found in the search query
            for tweet in tweepy.Cursor(api.search, q=keyword, lang="en").items():
                text = tweet.text
                time = tweet.created_at
                username = tweet.user.screen_name
                print(username + ':' + ' ' + text + ' ' + time)
        except tweepy.TweepError as e:
            print("Error: ", e)



keywords = ['coronavirus, COVID19, coronavirus uk']
users_list = ['realdonaldtrump', 'borisjohnson', 'bbcbreaking']
language = ['en']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Continuous stream of tweets
print("Starting Tweet Stream ")
stream = Stream(auth, StdOutListener())
stream.filter(track=keywords, languages=language)

# Rest API
print("Starting Rest API search")
rest_api(keywords, users_list)
