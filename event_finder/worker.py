import tweepy
from background_task import background
import datetime

from django.db.models import Max 

from event_finder.twitter_api.tokens import oauth_tokens, accesss_tokens
from event_finder.twitter_api import parsers 
from event_finder.models import Event
from event_finder.twitter_api.tests import TWEETS

def get_twitter_api():
    auth = tweepy.OAuthHandler(*oauth_tokens)
    auth.set_access_token(*accesss_tokens)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api 

def delete_old_events():
    thr = datetime.datetime.now() - datetime.timedelta(days=1)
    Event.objects.filter(datetime__lte=thr).delete()

@background(remove_existing_tasks=True, schedule=0)
def background_load_events_to_db():
    print("Background update")
    load_events_to_db()

def load_events_to_db():
    print("Real update DB")

    delete_old_events()
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
    delete_old_events()
    for tid, tweet in TWEETS:
        if not Event.objects.filter(id__exact=tid):
            parsed = parsers.parse_tweet(tid, tweet)
            e = Event(**parsed)
            e.save()

@background(remove_existing_tasks=True, schedule=0)
def background_load_dummy_events_to_db():
    print("Background update")
    load_dummy_events_to_db()


if __name__ == '__main__':
    load_events_to_db()