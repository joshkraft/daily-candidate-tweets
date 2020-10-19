import tweepy
import json
import os
import glob

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
    
    return api

def get_tweets_from_user(user):
    tweets = api.user_timeline(user, 
                               count = 10,
                               tweet_mode = 'extended')
    return tweets


def main():
    api = authenticate_with_secrets('/home/runner/secrets/secrets.json')
    

    usernames = ["realDonaldTrump", "JoeBiden"]

    for user in usernames:
        tweets = get_tweets_from_user(user)
        for tweet in tweets:
            print(tweet.created_at, tweet.full_text)

    """
    for user in usernames:
        file_path = "data/" + user + "/" + date + ".csv"
        tweets = fetch_and_process_tweets(user, date)
        upload_tweets(tweets, file_path)"""

if __name__ == "__main__":
    main()

