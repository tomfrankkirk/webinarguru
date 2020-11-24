import datetime
from event_finder.twitter_api.parsers import TweetParseError
from django.db.models import Max 
from django.utils import timezone

from event_finder.models import Event
from event_finder.twitter_api.tests import TWEETS
from event_finder.twitter_api import parsers
from event_finder.twitter_api.api import get_twitter_api

def time_now(): 
    now = datetime.datetime.now()
    return timezone.make_aware(now, 
            timezone.get_current_timezone(), is_dst=True)

def delete_all_events(): 
    Event.objects.all().delete()

def load_events_to_db():
    print("Real DB update")

    last_tweet = Event.objects.aggregate(Max('tweet_id'))
    # since_id=last_tweet['tweet_id__max']

    api = get_twitter_api()
    mentions = api.mentions_timeline(tweet_mode='extended', count=30)
    to_parse = zip([t.id for t in mentions], [t.full_text for t in mentions])

    parsed = 0 
    for tid, tweet_string in to_parse:
        if not Event.objects.filter(tweet_id=tid):
            try: 
                e = parsers.parse_tweet(tid, tweet_string)
                e = Event(**e)
                if e.datetime > time_now(): 
                    e.save()
                    parsed += 1 
            except TweetParseError as err: 
                print(f"\nSkipped: {tid}\n{tweet_string}")
                print(f"Error: {err}")
                pass 
            except Exception as err: 
                raise err
    print(f"Added {parsed} new events")

def load_dummy_events_to_db():
    print("Dummy update")

    for tid, tweet in TWEETS:
        if not Event.objects.filter(tweet_id=tid):
            parsed = parsers.parse_tweet(tid, tweet)
            e = Event(**parsed)
            if e.datetime > time_now():
                e.save()


def prune_events():
    api = get_twitter_api()

    # For any event that no longer has a corresponding tweet, 
    # delete (the event has been changed, and a new tweet will
    # probably appear at some point)
    for event in Event.objects.all(): 
        if not api.statuses_lookup([event.tweet_id]): 
            event.delete()

    # Delete old events 
    thr = time_now() - datetime.timedelta(days=1)
    Event.objects.filter(datetime__lte=thr).delete()