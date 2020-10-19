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
    api = tweepy.API(auth)
    return api

def get_tweets_from_user(api, user):
    tweets = api.user_timeline(user, 
                               count = 10,
                               tweet_mode = 'extended')
    return tweets

def upload_tweets(tweets, file_path):
    df = pd.DataFrame(tweets)
    return df.to_csv(file_path)


def main():
    api = authenticate_with_secrets('/home/runner/secrets/secrets.json')
    

    usernames = ["realDonaldTrump", "JoeBiden"]

    for user in usernames:
        file_path = "data/" + user + "/" + date + ".csv"
        tweets = get_tweets_from_user(api, user)
        for tweet in tweets:
            if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                print(tweet.created_at, tweet.full_text)

        upload_tweets(tweets, file_path)

    """
    for user in usernames:
        file_path = "data/" + user + "/" + date + ".csv"
        tweets = fetch_and_process_tweets(user, date)
        upload_tweets(tweets, file_path)"""

if __name__ == "__main__":
    main()

