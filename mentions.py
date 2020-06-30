import tweepy
import time
from tokens import oauth_tokens, accesss_tokens

if __name__ == '__main__':

	auth = tweepy.OAuthHandler(*oauth_tokens)
	auth.set_access_token(*accesss_tokens)
	api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	user = api.me()

	mentions = api.mentions_timeline()
	for mention in mentions:
		print(str(mention.id) + '-' + mention.text)
