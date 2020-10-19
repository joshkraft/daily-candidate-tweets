import tweepy
import json
import os
import glob
        
secret_file = open("/home/runner/secrets/secrets.json")
secret_data = json.load(secret_file)

CONSUMER_KEY = secret_data["API_KEY"] # does this need quotes?
CONSUMER_SECRET = secret_data["API_SECRET"]
ACCESS_TOKEN = secret_data["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = secret_data["ACCESS_SECRET"]

secret_file.close()
print('Found secrets.')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

trump_tweets = api.user_timeline('realDonaldTrump', 
                                 count = 10,
                                 tweet_mode = 'extended')
for tweet in trump_tweets:
    print(tweet.created_at, tweet.full_text)
