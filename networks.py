import pymongo
from pymongo import MongoClient
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from jgraph import *
from credentials import *


client = pymongo.MongoClient('127.0.0.1', 27017)
db = client.WebScience
tweets = db.WebScienceHour
tweets_list = tweets.find()
userlist = []


def get_followers(api):

    try:
        for tweet in tweets.find():
            userlist.append(tweet['username'])
            #print(tweet['username'])
    except OSError as e:
        print("ERROR:" + e)
        pass

    for username in userlist:
        user_objects = api.lookup_users(screen_names=username)
        userid = [user.id_str for user in user_objects]
        
    for user in userid:
        friendslist = api.lookup_friendships(user)    
        print("idk")
        print(friendslist)

    
    E = userid
    V = friendslist
    g = Graph(directed = true)
    g.add_vertices(V)
    g.add_edges(E)
    plot(g)



auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Rest API
print("Starting Rest API search")
get_followers(api)
