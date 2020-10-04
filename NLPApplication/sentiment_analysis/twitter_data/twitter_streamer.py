

import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from . import twitter_credentials as keys


# Create twitter_credentials.py file in current and using
# the below naming conventions to variables
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
        auth.set_access_token(keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
        return auth

class GetAPI:

    def get_api(self):
        return tweepy.API( TwitterAuthenticator().authenticate_twitter_app() )

class GetTweets:

    def __init__(self):
        self.api = GetAPI().get_api()

    def get_user_tweets(self, username, no_of_tweets):
        tweets = []
        try:
            for tweet in Cursor(self.api.user_timeline, id = username).items(no_of_tweets):
                tweets.append(tweet.text)
        except Exception as e:
            return ['Exception Occur in Loading data', str(e)]
        return tweets

    def get_hashtag_tweets(self, hashtag, no_of_tweets):
        tweets = []
        try:
            for tweet in Cursor(self.api.search, q = hashtag).items(no_of_tweets):
                tweets.append(tweet.text)
        except Exception as e:
            return ['Exception Occur in Loading data', str(e)]
        return tweets