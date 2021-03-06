import pymongo
from pymongo import MongoClient
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import adjusted_rand_score


client = pymongo.MongoClient('127.0.0.1', 27017)
db = client.WebScience
tweets = db.WebScienceHour
tweets_list = tweets.find()


def tweet_text_cluster(tweets_list):
    tweetArray = []
    print("Starting Text Clustering")
    try:
        for tweet in tweets.find():

            tweetArray.append(tweet['text'])
    except OSError as e:
        print("ERROR:" + e)
        pass

    vectorizer = TfidfVectorizer(stop_words='english') 
    X = vectorizer.fit_transform(tweetArray)

    cluster_no = 10
    model = KMeans(n_clusters=cluster_no, init='k-means++',
                   max_iter=100, n_init=1)
    model.fit(X)

    print("Top terms per text cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(cluster_no):
        print("Cluster %d: " % (i+1)),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),
            print
    print("\n")


def tweet_author_cluster(tweets_list):
    authorArray = []
    print("Starting username clustering")
    try:
        for tweet in tweets.find():
            authorArray.append(tweet['username'])
    except OSError as e:
        print("ERROR:" + e)
        pass

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(authorArray)

    cluster_no = 10
    model = KMeans(n_clusters=cluster_no, init='k-means++',
                   max_iter=100, n_init=1)
    model.fit(X)

    print("Top terms per username cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(cluster_no):
        print("Cluster %d: " % (i+1)),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),
            print
    print("\n")


def tweet_hashtag_cluster(tweets_list):
    hashtagArray = []
    print("Starting hashtag clustering")
    try:
        for tweet in tweets.find():
            hashtags = tweet['hashtags']
            if hashtags != []:
                hashtagArray.append(hashtags[0].get('text'))
    except OSError as e:
        print("ERROR:" + e)
        pass

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(hashtagArray)

    cluster_no = 10
    model = KMeans(n_clusters=cluster_no, init='k-means++',
                   max_iter=100, n_init=1)
    model.fit(X)

    print("Top terms per hashtag cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(cluster_no):
        print("Cluster %d: " % (i+1)),
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind]),
            print
    print("\n")

print("Starting clustering process - may take some time")
tweet_text_cluster(tweets_list)
tweet_author_cluster(tweets_list)
tweet_hashtag_cluster(tweets_list)
