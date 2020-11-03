import tweepy
import datetime
from django.db.models import Max 
from django.utils import timezone

from webinarguru.settings import TWITTER_ACCESS_TOKENS, TWITTER_OAUTH_TOKENS
from event_finder.twitter_api import parsers 
from event_finder.models import Event
from event_finder.twitter_api.tests import TWEETS

def time_now(): 
    now = datetime.datetime.now()
    return timezone.make_aware(now, 
            timezone.get_current_timezone(), is_dst=True)

def get_twitter_api():
    auth = tweepy.OAuthHandler(*TWITTER_OAUTH_TOKENS)
    auth.set_access_token(*TWITTER_ACCESS_TOKENS)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api 

def delete_old_events():
    thr = time_now() - datetime.timedelta(days=1)
    Event.objects.filter(datetime__lte=thr).delete()

def delete_all_events(): 
    Event.objects.all().delete()

def load_events_to_db():
    print("Real DB update")

    delete_all_events()
    api = get_twitter_api()
    mentions = api.mentions_timeline(tweet_mode='extended', count=20)
    to_parse = zip([t.id for t in mentions], [t.full_text for t in mentions])

    parsed = 0 
    for tid, tweet_string in to_parse:
        if not Event.objects.filter(tweet_id=tid):
            try: 
                parsed = parsers.parse_tweet(tid, tweet_string)
                event = Event(**parsed)
                event.save()
                parsed += 1 
            except RuntimeError as e: 
                print(f"\nSkipped: {tid}\n")
                pass 
            except Exception as e: 
                raise e
        else: 
            parsed += 1
    print("parsed: ", parsed, "out of", len(mentions))

def load_dummy_events_to_db():
    print("Dummy update")
    delete_all_events()
    for tid, tweet in TWEETS:
        import pdb; pdb.set_trace()
        if not Event.objects.filter(tweet_id=tid):
            parsed = parsers.parse_tweet(tid, tweet)
            e = Event(**parsed)
            if e.datetime > time_now():
                e.save()

