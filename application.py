import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd
load_dotenv(dotenv_path='.env')
# get bearer_key from .env file
bearer_token = os.environ["BEARER_KEY"]
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = "AAAAAAAAAAAAAAAAAAAAAJdDaQEAAAAAh%2FezfGwa9sJo1g9PeVlvIO2g3Ic%3DTAyvL8VKOS7zDe5lXtB3tXyCAFMMiaAdTiBz8eyTebp4ElMPtx"

usernames = pd.read_excel('data.xlsx', sheet_name='Sheet1')['REAL NAME']
print(usernames)


# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {
    'query': 'NFT -is:retweet -is:reply', 'tweet.fields': 'author_id', 'max_results': 10}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main(following, followers, tweet_Count):

    for username in usernames:
        username = username.strip()  # remove whitespace
        profile_url = "https://api.twitter.com/2/users/by/username/{}?user.fields=public_metrics".format(
            username.replace("@", ""))

        json_response = requests.get(
            profile_url, auth=bearer_oauth).json().get("data")
        id = json_response.get("id")

    # get all the author_id from the json response
    # author_ids = [tweet.get("author_id") for tweet in json_response]
        print(json.dumps(id, indent=4, sort_keys=True))

    # for author_id in author_ids:
    #     user_url = f"https://api.twitter.com/2/users/{author_id}?user.fields=public_metrics"
    #     user_response = requests.get(user_url, auth=bearer_oauth).json()
    #     print(json.dumps(user_response, indent=4, sort_keys=True))


if __name__ == "__main__":

    # get all the number of followers and following
    followers = []
    following = []
    tweet_Count = []
    main(followers, following, tweet_Count)
