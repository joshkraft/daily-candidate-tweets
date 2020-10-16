import requests
import pandas as pd
import json
import ast
import yaml
from github import Github

TRUMP_USERNAME = "realDonaldTrump"
BIDEN_USERNAME = "JoeBiden"

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
    res_json = twitter_auth_and_connect(bearer_token, url)
    print(res_json)

def create_github_token(data):
    return data["github_api"]["pat"]




def main():
    #get_tweets_for_user(TRUMP_USERNAME)
    print('Main Ran')
    data = process_yaml()
    github_token = create_github_token(data)
    g = Github(github_token)

    repo = g.get_repo("joshkraft/daily-candidate-tweets")
    contents = repo.get_contents("README.md")
    print(contents)



if __name__ == "__main__":
    main()