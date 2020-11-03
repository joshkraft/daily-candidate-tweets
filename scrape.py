import pandas as pd
import datetime
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

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    return api


def get_yesterdays_date():
    yesterdays_datetime = datetime.datetime.today() + datetime.timedelta(days=-1)
    yesterdays_date = yesterdays_datetime.strftime('%Y-%m-%d')
    return str(yesterdays_date)


def get_last_tweet_ids():
    with open("most_recent_tweet_id.json", "r") as file:
        return json.load(file)


def update_last_tweet_ids(last_tweet_ids):
    with open("most_recent_tweet_id.json", "w") as file:
        json.dump(last_tweet_ids, file)


def get_tweets_from_user(api, user, last_tweet_ids):
    if user in last_tweet_ids:
        most_recent_tweet_id = int(last_tweet_ids[user])
        tweets = api.user_timeline(user, 
                                   since_id = most_recent_tweet_id + 1,
                                   include_rts = False,
                                   tweet_mode = 'extended')
    if tweets:
        last_tweet_ids[user] =  str(tweets[0].id)
        return tweets
    else:
        print('No tweets pulled for ' + user + '. Check recent tweet id.')


def upload_tweets(tweets, file_path):
    df = pd.DataFrame(tweets)
    return df.to_csv(file_path)


def main():
    api = authenticate_with_secrets('/home/runner/secrets/secrets.json')
    usernames = ["realDonaldTrump", "JoeBiden"]

    last_tweet_ids = get_last_tweet_ids()

    for user in usernames:
        file_path = "data/" + user + "/data.csv"
        processed_tweets = []
        tweets = get_tweets_from_user(api, user, last_tweet_ids)
        if tweets:
            for tweet in tweets:
                tweet_details = {}
                tweet_details['id'] = tweet.id
                tweet_details['username'] = tweet.user.screen_name
                tweet_details['tweet_text'] = tweet.full_text
                tweet_details['retweets'] = tweet.retweet_count
                tweet_details['location'] = tweet.user.location
                tweet_details['created_at'] = tweet.created_at
                processed_tweets.append(tweet_details)
            upload_tweets(processed_tweets, file_path)
    update_last_tweet_ids(last_tweet_ids)

if __name__ == "__main__":
    main()

