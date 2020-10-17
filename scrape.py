import requests
import pandas as pd
import json
import ast
import yaml
from github import Github
import datetime
import csv
import os

USERNAMES = ["realDonaldTrump", "JoeBiden"]

def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()


def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)


def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]


def create_twitter_url(handle):
    handle = handle
    max_results = 10
    mrf = "max_results={}".format(max_results)
    q = "query=from:{}".format(handle)
    url = "https://api.twitter.com/2/tweets/search/recent?tweet.fields=created_at&{}&{}".format(
        mrf, q
    )
    return url


def get_tweets_for_user(username):
    url = create_twitter_url(username)
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    tweet_json = twitter_auth_and_connect(bearer_token, url)
    return tweet_json

def extract_tweets_from_today(tweet_json):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    tweet_data = [tweet_json['data']]
    tweet_list = []
    for tweets in tweet_data:
        for tweet in tweets:
            if tweet['created_at'][0:10] == today:
                tweet_list.append(tweet)
    return tweet_list

def create_github_token():
    data = process_yaml()
    return data["github_api"]["pat"]

def fetch_and_process_tweets(username):
    tweet_json = get_tweets_for_user(username)
    tweets = extract_tweets_from_today(tweet_json)
    return tweets

def create_tweets_file(tweets, file_path):
    df = pd.DataFrame(tweets)
    df.to_csv(file_path)
    """if not os.path.isfile(file_path):
       df.to_csv(file_path)
    else: # else it exists so append without writing the header
        df.to_csv(file_path, mode='a', header=False)"""
        




def main():
    g = Github(create_github_token())
    repo = g.get_repo("joshkraft/daily-candidate-tweets")
    for user in USERNAMES:
        file_path = "./data/" + user + "/" + str(datetime.date.today()) + ".csv"
        tweets = fetch_and_process_tweets(user)
        #create_tweets_file(tweets, file_path)
        repo_contents = repo.get_contents(file_path)
        print(repo_contents == True)
        
        


        



if __name__ == "__main__":
    main()