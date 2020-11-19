from datetime import datetime
import re 
from urllib.parse import urlparse
from urllib.parse import urlparse
from dateutil.parser import parse as parse_datetime
import itertools

from django.forms import URLField
from django.core.exceptions import ValidationError
from django.utils import timezone

from .api import get_twitter_api

DF_COLUMNS = ['title', 'datetime', 'link', 'hashtags', 'tweet_id']

TZ = timezone.get_current_timezone() 

class TweetParseError(Exception):
    pass 

def parse_time(string):

    time = None 
    
    time_digits = re.findall(r'\d', string)
    if len(time_digits) == 4: 
        time = "".join(time_digits)

    elif string.count('am') or string.count('pm'): 
        time = re.match(r'\d*(am)?(pm)?', string).group()
            
    elif re.match(r'\d*[\.\:\sh]{1}(\d)?', string):
        time = re.match(r'\d*[\.\:\sh,]{1}(\d)?', string).group()

    if time: 
        time = int("".join(re.findall('\d', time)))
        if time < 100: time *= 100
        if string.count('pm') and (time < 1159): time += 1200 
        return f"{time:04d}"

    else: 
        return None 


def validate_url(url):
    url_form_field = URLField()
    try:
        url_form_field.clean(url)
    except ValidationError:
        return False
    return True


def parse_tweet_by_id(tweet_id):
    
    api = get_twitter_api()
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    assert tweet, 'No tweet returned for id %s' % tweet_id
    return parse_tweet(tweet.id, tweet.full_text)


def parse_tweet(tid, string):

    # Split the tweet into single words 
    raw_text = string.replace("\n", " ").split()

    # Store results in dict 
    out = dict(zip(DF_COLUMNS, itertools.repeat(None)))
    out['datetime'] = []
    hashtags = []
    title = []
    finished_title = False

    for fragment in raw_text: 

        # If its got a hash, its something important 
        # This also means we have finished extracting the title 
        if fragment.count("#"):
            finished_title = True 
            f = fragment.strip("#")

            # Try and parse as a combined datetime first 
            try: 
                dt = parse_datetime(f, fuzzy=True)
                out['datetime'].append(dt) 
                if len(out['datetime']) > 2: 
                    raise TweetParseError("Parsed more than two datetimes")
                continue 

            except TweetParseError as e: 
                raise e 
            except Exception:
                pass 

            # If that didn't work, try and parse it as a time 
            time = parse_time(f)
            if time: 
                if ('time' in out) and (out['time'] is not None): 
                    raise TweetParseError("Multiple times found")
                out['time'] = time
                continue 

            # If that didn't work, its probably just a hashtag
            hashtags.append(fragment)
            continue

        # No hashtag - could be a website 
        if validate_url(fragment): 
            if out['link'] is not None: 
                raise TweetParseError("Multiple weblinks found")
            out['link'] = fragment
            continue 

        # Anything else; probably raw text from title 
        if not fragment.count('@') and (not finished_title):
            title.append(fragment)

    # If we didn't get a title, datetime and link, give up 
    if not all([title, bool(out['datetime']), out['link']]):
        raise TweetParseError("Could not parse tweet") 

    # If we parsed two datetime objects, then assume one of them 
    # represents time and the other date. We need to merge the time
    # one into the date one. The time one will have had its date set
    # as today, so use that condition to detect them. 
    if len(out['datetime']) > 1: 
        first, second = out['datetime']
        today = datetime.today().date()
        if (first.date() == today) and (second.date() != today): 
            final_datetime = datetime.combine(second.date(), first.time()) 
        elif (second.date() == today) and (first.date() != today):
            final_datetime = datetime.combine(first.date(), second.time()) 
        elif (first.date() == today) and (second.date() == today): 
            # they are both dated today - the one with the later time
            # is the pertinent one because the pure date one will
            # start at midnight
            final_datetime = first if first > second else second 
        else: 
            raise TweetParseError("Could not merge two datetimes")

    elif not out['datetime'][0].hour: 
        time = out.pop('time')
        date = out.pop('datime')[0]
        final_datetime = date.replace(
            hour=int(time[:2]), minute=int(time[2:]))

    else: 
        final_datetime = out.pop('datetime')[0]
        if not final_datetime.hour == 0: 
            raise TweetParseError('Event at midnight')

    out['datetime'] = final_datetime
    out['title'] = " ".join(title)
    out['hashtags'] = " ".join(hashtags)
    out['tweet_id'] = tid
    out['datetime'] = timezone.make_aware(out['datetime'], TZ, True)

    return out 