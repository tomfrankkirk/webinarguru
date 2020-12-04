# Webinar guru

Twitter bot for finding webinars: [www.medx.guru](#www.medx.guru)

## How does it work?

Tweets us @webinarg with something in the following form: 
```
the tile of the talk, as long as you want
#date #time 
#extra #hashtags 
some_weblink.com 
@webinarg
```

For example: 
```
my webinar about stuff #10Dec #8pm #medicine #hospitals my_website.com @webinarg
```

Strictly speaking, the order of the hashtags and link at the bottom don't really matter too much, but the tilte *must* come before them.

Do we want to record the extra @mentions?

Google sheets interface: 
enable the drive and sheets API on the google developer console. 
create a service account, which has a specific email associated with it 
share the relevant sheets with the service account by using this email address 

## Notes:

Use `tweet_mode='extended'` for all tweepy API calls that return `Status` objects to ensure text isn't clipped down to 140 chars. 

Catching duplicate events: can we distinguish between the original tweet that @mentions us, and gives the event info, and anyone else who is simply re-tweeting someone elses tweet?
use api.retweets() gives the first 100 retweets of a given tweet. add field to model to store retweets?
provide weblink on index page to the origin tweet on twitter
if tweet is retweet, it contains property named 'retweeted_status' 
when parsing tweets, add a check for datetime (don't parse old tweets)