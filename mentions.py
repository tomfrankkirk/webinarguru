import time
import pickle 
import datetime 
import dateutil 

import parsers

import tweepy
from tokens import oauth_tokens, accesss_tokens



if __name__ == '__main__':

    auth = tweepy.OAuthHandler(*oauth_tokens)
    auth.set_access_token(*accesss_tokens)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.me()

    # mentions = api.mentions_timeline(tweet_mode='extended')
    with open('dummy.pkl', 'rb') as f: 
        mentions = [ pickle.load(f) ]

    for mention in reversed(mentions):
        print(str(mention.user.name))
        print(mention.full_text)
        print("")
        if mention.user.name == 'Rob Staruch':
            parsers.parse_tweet(mention)

