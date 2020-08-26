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

Google sheets interface: 
enable the drive and sheets API on the google developer console. 
create a service account, which has a specific email associated with it 
share the relevant sheets with the service account by using this email address 

## Notes:

Use `tweet_mode='extended'` for all tweepy API calls that return `Status` objects to ensure text isn't clipped down to 140 chars. 