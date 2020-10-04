from django.shortcuts import render, redirect
from  django.urls import reverse
from .twitter_data import twitter_credentials as private_keys
from .ml_models import GetTweets, PreProcessing

from pymongo import MongoClient

import pickle
import os
import datetime
import numpy as np

client = MongoClient(private_keys.CLIENT)
db = client[private_keys.DB]
collection = db[private_keys.COLLECTION]

def home(request):
    if request.method == "POST":
        if 'query-type' in request.POST and 'message' in request.POST:
            query_type = request.POST['query-type']
            message = request.POST['message']
            unique_id = message + '_' + str( datetime.datetime.now() )

            if query_type == "single_tweet":
                tweet_count = np.int16(1)
                total_tweets = [message]
                clean_tweets = PreProcessing.Preprocessing().get_preprocessed_tweets(total_tweets)

                folder_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                pkl_filename = os.path.join(folder_dir, 'sentiment_analysis\ml_models\\tfid.pickle')
                with open(pkl_filename, 'rb') as file:  
                    tfidft = pickle.load(file)
                tfidft_dtm = tfidft.transform(clean_tweets)

                pkl_filename = os.path.join(folder_dir, 'sentiment_analysis\ml_models\lrg.pickle')
                with open(pkl_filename, 'rb') as file:  
                    lrg = pickle.load(file)

                results = lrg.predict(tfidft_dtm)
            else:
                tweet_count = request.POST['count']
                tweet_count = np.array(int(tweet_count))
                total_tweets = []
                if query_type == 'hashtag':
                    total_tweets  = GetTweets.GetTweets(private_keys.CONSUMER_KEY, private_keys.CONSUMER_SECRET,
                    private_keys.ACCESS_TOKEN, private_keys.ACCESS_TOKEN_SECRET).get_hashtag_tweets(message, tweet_count)
                else:
                    total_tweets  = GetTweets.GetTweets(private_keys.CONSUMER_KEY, private_keys.CONSUMER_SECRET,
                    private_keys.ACCESS_TOKEN, private_keys.ACCESS_TOKEN_SECRET).get_user_tweets(message, tweet_count)

                clean_tweets = PreProcessing.Preprocessing().get_preprocessed_tweets(total_tweets)

                folder_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                pkl_filename = os.path.join(folder_dir, 'sentiment_analysis\ml_models\\tfid.pickle')
                with open(pkl_filename, 'rb') as file:  
                    tfidft = pickle.load(file)
                tfidft_dtm = tfidft.transform(clean_tweets)

                pkl_filename = os.path.join(folder_dir, 'sentiment_analysis\ml_models\lrg.pickle')
                with open(pkl_filename, 'rb') as file:  
                    lrg = pickle.load(file)

                results = lrg.predict(tfidft_dtm)

            
            for i in range(tweet_count.astype(int)):
                document = {
                    'message_id' :unique_id,
                    'message':message,
                    'tweet' : query_type,
                    'tweet' : total_tweets[i],
                    'label' : results[i].astype(str)
                }
                collection.insert_one(document)

            context = {
                'data' : collection.find( { 'message_id' : unique_id } )
            }
            return result(request, context)

    else:
        return render(request, "sentiment_analysis/home.html")


def result(request,context={}):
    
    return render(request, 'sentiment_analysis/result.html', context=context)
