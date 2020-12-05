from datetime import date, datetime, timedelta

from .api import get_twitter_api
from event_finder.models import Event
from event_finder.db_updates import time_now
from webinarguru.settings import DEBUG

RETWEET_TIME_HRS = timedelta(hours=24)
UPDATE_FREQ_MINS = 10

def retweet_events(): 
    api = get_twitter_api()
    now = time_now()
    for event in Event.objects.all(): 
        # 24h beforehand, we want to retweet. But because this code runs
        # every 10 mins, we want to make sure we are within 10 mins of the 
        retweet_time = event.datetime - RETWEET_TIME_HRS
        time_till_retweet = retweet_time - now 
        mins_till_retweet = ((24 * 60 * time_till_retweet.days) 
                            + (time_till_retweet.seconds / 60))

        if ((mins_till_retweet <= UPDATE_FREQ_MINS) 
            and (mins_till_retweet > 0)): 
            if DEBUG:
                print("Retweeting", event.tweet_id)
            else:
                try: 
                    api.retweet(event.tweet_id)
                except Exception: 
                    print(f"WARNING: could not retweet {event.tweet_id}")

