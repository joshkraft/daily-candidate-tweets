import tweepy
import json
import os
import glob

"""

# LOCAL METHOD
import secrets

CONSUMER_KEY = secrets.CONSUMER_KEY
CONSUMER_SECRET = secrets.CONSUMER_SECRET
ACCESS_TOKEN = secrets.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = secrets.ACCESS_TOKEN_SECRET
"""

# ACTIONS METHOD

for root, dirs, files in os.walk("."):
    for filename in files:
        print(filename)
        
secret_file = open('secrets/secrets.json')
secret_data = json.load(secret_file)
print('Found secrets.')

"""CONSUMER_KEY = os.getenv('INPUT_CONSUMER_KEY') # does this need quotes?
CONSUMER_SECRET = os.getenv('INPUT_CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('INPUT_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('INPUT_ACCESS_TOKEN_SECRET')"""

"""print(CONSUMER_KEY)
print(CONSUMER_SECRET)
print(ACCESS_TOKEN)
print(ACCESS_TOKEN_SECRET)"""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

trump_tweets = api.user_timeline('realDonaldTrump', 
                                 count = 10,
                                 tweet_mode = 'extended')
for tweet in trump_tweets:
    print(tweet.created_at, tweet.full_text)
