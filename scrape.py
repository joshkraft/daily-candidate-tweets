from github import Github
import pandas as pd
import datetime
import requests
import json
import yaml
import csv
import os

def get_yesterdays_date():
    yesterdays_datetime = datetime.datetime.today() + datetime.timedelta(days=-1)
    yesterdays_date = yesterdays_datetime.strftime('%Y-%m-%d')
    return str(yesterdays_date)

def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()

def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)

def create_bearer_token():
    return os.getenv('INPUT_TWITTER_TOKEN')
    #return data["search_tweets_api"]["bearer_token"]

def create_twitter_url(handle):
    handle = handle
    max_results = 100
    mrf = "max_results={}".format(max_results)
    q = "query=from:{}".format(handle)
    url = "https://api.twitter.com/2/tweets/search/recent?tweet.fields=created_at&{}&{}".format(
        mrf, q
    )
    return url

def get_tweets_for_user(username):
    url = create_twitter_url(username)
    bearer_token = create_bearer_token()
    tweet_json = twitter_auth_and_connect(bearer_token, url)
    return tweet_json

def drop_tweets_outside_date(tweet_json, date):
    tweet_data = [tweet_json['data']]
    tweet_list = []
    for tweets in tweet_data:
        for tweet in tweets:
            if tweet['created_at'][0:10] == date:
                tweet_list.append(tweet)
    return tweet_list

def fetch_and_process_tweets(username, date):
    tweet_json = get_tweets_for_user(username)
    tweets = drop_tweets_outside_date(tweet_json, date)
    return tweets

def upload_tweets(tweets, file_path):
    df = pd.DataFrame(tweets)
    return df.to_csv(file_path)

def main():
    usernames = ["realDonaldTrump", "JoeBiden"]
    date = get_yesterdays_date()
    
    for user in usernames:
        file_path = "data/" + user + "/" + date + ".csv"
        tweets = fetch_and_process_tweets(user, date)
        upload_tweets(tweets, file_path)

if __name__ == "__main__":
    main()