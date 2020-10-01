import tweepy
import time
from tokens import oauth_tokens, accesss_tokens

def main(api):

	search = '#webinarg'
	nrTweets = 500	

	for tweet in tweepy.Cursor(api.search, search).items(nrTweets):
		try:
			print('Retweeted')
			tweet.retweet()
			time.sleep(10)
		except tweepy.TweepError as e:
			print(e.reason)
		except StopIteration:
			break

	for follower in tweepy.Cursor(api.followers).items():
		follower.follow()


if __name__ == '__main__':

	auth = tweepy.OAuthHandler(*oauth_tokens)
	auth.set_access_token(*accesss_tokens)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	user = api.me()
	main(api)
