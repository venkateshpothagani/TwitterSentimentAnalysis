import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer


class PreprocessingMethods:
    
    pattern = r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)'
        
    def tweet_cleaning(self, tweet):
        return ' '.join(re.sub(self.pattern,'',tweet).split())
    
    
    def normalization(self, tweet):
        lem = WordNetLemmatizer()
        stemmer = PorterStemmer()
        normalized_tweet = []
        for word in tweet.split():
            normalized_text = lem.lemmatize(word,'v')
            normalized_tweet.append( stemmer.stem(normalized_text) )
        return normalized_tweet
 
    def remove_stopwords(self, tweet):
        return [ word for word in tweet if word not in (stopwords.words('english')) ]
    


class Preprocessing:
    
    def __init__(self):
        self.preprocessing_methods_obj = PreprocessingMethods
        
    def get_preprocessed_tweets(self, tweets):
        
        preprocessed_tweets = []
        
        for tweet in tweets:
            cleaned_tweet = PreprocessingMethods().tweet_cleaning(tweet)
            normalized_tweet = PreprocessingMethods().normalization(cleaned_tweet)
            preprocessed_tweet = PreprocessingMethods().remove_stopwords(normalized_tweet)
            preprocessed_tweets.append( ' '.join(preprocessed_tweet) )
        
        return preprocessed_tweets