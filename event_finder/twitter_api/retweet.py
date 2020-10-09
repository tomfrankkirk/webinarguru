import tweepy
import time

# def main(api):

# 	search = '#webinarg'
# 	nrTweets = 500	

# 	for tweet in tweepy.Cursor(api.search, search).items(nrTweets):
# 		try:
# 			print('Retweeted')
# 			tweet.retweet()
# 			time.sleep(10)
# 		except tweepy.TweepError as e:
# 			print(e.reason)
# 		except StopIteration:
# 			break

# 	for follower in tweepy.Cursor(api.followers).items():
# 		follower.follow()

