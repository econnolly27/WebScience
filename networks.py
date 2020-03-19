import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient('127.0.0.1',27017)
db = client.WebScience
tweets = db.WebScienceHour
tweets_list = tweets.find()

print(tweets_list[9])