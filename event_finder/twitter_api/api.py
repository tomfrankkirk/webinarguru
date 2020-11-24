import tweepy

from webinarguru.settings import TWITTER_ACCESS_TOKENS, TWITTER_OAUTH_TOKENS, DEBUG
from event_finder.twitter_api import parsers 

def get_twitter_api():
    auth = tweepy.OAuthHandler(*TWITTER_OAUTH_TOKENS)
    auth.set_access_token(*TWITTER_ACCESS_TOKENS)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api 

