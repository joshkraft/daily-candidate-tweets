
last_retrieved_tweet_ids = {}


def get_tweets_from_user(api, user):
    tweets = [123, 4526]
    
    updated_id = {user: str(tweets[-1])}
    last_retrieved_tweet_ids.update(updated_id)

get_tweets_from_user('api', 'trump')

print(last_retrieved_tweet_ids)