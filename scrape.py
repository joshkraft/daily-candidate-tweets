import pandas as pd
import datetime
import tweepy
import json
import os
import glob

def get_yesterdays_date():
    yesterdays_datetime = datetime.datetime.today() + datetime.timedelta(days=-1)
    yesterdays_date = yesterdays_datetime.strftime('%Y-%m-%d')
    return str(yesterdays_date)

def authenticate_with_secrets(secret_filepath):
    secret_file = open(secret_filepath)
    secret_data = json.load(secret_file)
    CONSUMER_KEY = secret_data["API_KEY"]
    CONSUMER_SECRET = secret_data["API_SECRET"]
    ACCESS_TOKEN = secret_data["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = secret_data["ACCESS_SECRET"]
    secret_file.close()
    print('Found secrets.')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def get_tweets_from_user(api, user):
    tweets = api.user_timeline(user, 
                               count = 200,
                               tweet_mode = 'extended')
    return tweets

def upload_tweets(tweets, file_path):
    df = pd.DataFrame(tweets)
    return df.to_csv(file_path)

def process_tweets(all_tweets):
    processed_tweets = []
    for tweet in all_tweets:
        if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
            processed_tweets.append(tweet)

    return processed_tweets

def main():
    api = authenticate_with_secrets('/home/runner/secrets/secrets.json')
    date = get_yesterdays_date()
    usernames = ["realDonaldTrump", "JoeBiden"]

    for user in usernames:
        file_path = "data/" + user + "/" + date + ".csv"
        for tweet in get_tweets_from_user(api, user):
            print(tweet)
            print(tweet['retweeted'])
        """json_tweets = [t._json for t in raw_tweets]
        tweet_df = pd.io.json.json_normalize(json_tweets)
        
        tweet_df = tweet_df[tweet_df['retweeted'] == 0]

        upload_tweets(tweet_df, file_path)"""

        

    """
    for user in usernames:
        file_path = "data/" + user + "/" + date + ".csv"
        tweets = fetch_and_process_tweets(user, date)
        upload_tweets(tweets, file_path)"""

if __name__ == "__main__":
    main()

