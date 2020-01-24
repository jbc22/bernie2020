import tweepy
from collections import Counter
from datetime import datetime, date, time, timedelta
import sys
import json
import os
import io
import re
import time
import googlemaps

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

google_api_key=""

# Helper functions to load and save intermediate steps
def save_json(variable, filename):
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(str(json.dumps(variable, indent=4, ensure_ascii=False)))

# Get a list of follower ids for the target account
def get_followers(target):
    api = tweepy.API(tweepy.auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    #Below code will request for 5000 follower ids in one request and therefore will give 75K ids in every 15 minute window (as 15 requests could be made in each window).
    followerids =[]
    for user in tweepy.Cursor(api.followers_ids, screen_name=target,count=5000).items():
        followerids.append(user)    
    print (len(followerids))
    return ids

if __name__ == "__main__": 
    account_list = [] 
    if (len(sys.argv) > 1):
        account_list = sys.argv[1:]

    if len(account_list) < 1:
        print("No parameters supplied. Exiting.")
        sys.exit(0)

    tweepy.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    tweepy.auth.set_access_token(access_token, access_token_secret)
    tweepy.auth_api = tweepy.API(tweepy.auth)

    for target in account_list:
        print("Processing target: " + target)

    results = get_followers(target)
    print(dir(results))
    print("Number of followers gathered: " + results)
    
    print("Follower screen name, Follower Location")
    for follower in results:
        # Ensure the follower has their location filled in
        if follower.location:

            # Use Google Maps API to ensure the location is valid
            gmaps = googlemaps.Client(google_api_key)
            try:
                geocode_result = gmaps.geocode(follower.location)

                # If the location is valid, print the follower and their location
                if geocode_result:
                    print(follower.screen_name + ", " + follower.location)
                    print(geocode_result)
            except:
                pass