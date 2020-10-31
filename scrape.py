import pandas as pd
import datetime
import tweepy
import json
import os
import glob


last_retrieved_tweet_ids = {}

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

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    return api


def get_tweets_from_user(api, user, most_recent_tweet_id_dict):
    if user in most_recent_tweet_id_dict:
        tweets = api.user_timeline(user, 
                                   count = 200,
                                   max_id = most_recent_tweet_id_dict[user] - 1,
                                   include_rts = False,
                                   tweet_mode = 'extended')
    else:
        tweets = api.user_timeline(user, 
                                   count = 200,
                                   include_rts = False,
                                   tweet_mode = 'extended')
    most_recent_tweet_id_dict[user] =  str(tweets[-1].id)
    return tweets

def upload_tweets(tweets, file_path):
    df = pd.DataFrame(tweets)
    return df.to_csv(file_path)

def fromYesterday(tweet, yesterdays_date):
    return tweet.created_at.strftime('%Y-%m-%d') == yesterdays_date

def notRetweet(tweet):
    return (tweet.retweeted == False) and ('RT @' not in tweet.full_text)

def get_last_tweet_ids():
    with open("most_recent_tweet_id.json", "r") as file:
        most_recent_tweet_id_dict = json.load(file)

def write_last_tweet_ids():
    with open("most_recent_tweet_id.json", "w") as file:
        json.dump(most_recent_tweet_id_dict, file)

def main():
    api = authenticate_with_secrets('/home/runner/secrets/secrets.json')
    yesterdays_date = get_yesterdays_date()
    usernames = ["realDonaldTrump", "JoeBiden"]

    get_last_tweet_ids()

    for user in usernames:
        file_path = "data/" + user + "/" + yesterdays_date + ".csv"
        processed_tweets = []
        for tweet in get_tweets_from_user(api, user, most_recent_tweet_id_dict):
            tweet_details = {}
            if notRetweet(tweet) and fromYesterday(tweet, yesterdays_date):
                tweet_details['username'] = tweet.user.screen_name
                tweet_details['tweet_text'] = tweet.full_text
                tweet_details['retweets'] = tweet.retweet_count
                tweet_details['location'] = tweet.user.location
                tweet_details['created_at'] = tweet.created_at
                processed_tweets.append(tweet_details)

        upload_tweets(processed_tweets, file_path)

    write_last_tweet_ids()

if __name__ == "__main__":
    main()

