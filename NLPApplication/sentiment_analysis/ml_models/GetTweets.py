import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class GetTweets:

    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API( auth )

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