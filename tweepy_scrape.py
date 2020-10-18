import tweepy
import os

"""

# LOCAL METHOD
import secrets

CONSUMER_KEY = secrets.CONSUMER_KEY
CONSUMER_SECRET = secrets.CONSUMER_SECRET
ACCESS_TOKEN = secrets.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = secrets.ACCESS_TOKEN_SECRET
"""

# ACTIONS METHOD

CONSUMER_KEY = os.getenv(CONSUMER_KEY) # does this need quotes?
CONSUMER_SECRET = os.getenv(CONSUMER_SECRET)
ACCESS_TOKEN = os.getenv(ACCESS_TOKEN)
ACCESS_TOKEN_SECRET = os.getenv(ACCESS_TOKEN_SECRET)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

trump_tweets = api.user_timeline('realDonaldTrump', 
                                 count = 10,
                                 tweet_mode = 'extended')
for tweet in trump_tweets:
    print(tweet.created_at, tweet.full_text)
