# Webinar guru

Twitter bot for finding webinars 

## How does it work?

Tweets need to be in the following form: 
```
the tile of the talk 
#date #time 
#extra #hashtags 
some_weblink.com 
@webinarguru
```

Strictly speaking, the order of the hashtags and link at the bottom don't really matter too much, but the tilte *must* come before them.

Do we want to record the extra @mentions?

## Notes:

Use `tweet_mode='extended'` for all tweepy API calls that return `Status` objects to ensure text isn't clipped down to 140 chars. 