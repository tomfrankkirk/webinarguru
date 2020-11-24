from event_finder import db_updates
from event_finder.twitter_api import parsers, retweet
from webinarguru.settings import DEBUG

def run():
    print("debug:", DEBUG)
    if DEBUG:
        parsers.test_against_current_db()
    db_updates.prune_events()
    # db_updates.load_dummy_events_to_db()
    db_updates.load_events_to_db()
    # parsers.parse_tweet_by_id(1329415689657049088)
    # retweet.retweet_events()