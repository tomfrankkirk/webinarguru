import re 
from urllib.parse import urlparse
from urllib.parse import urlparse
from dateutil.parser import parse as parse_datetime
import itertools

from django.forms import URLField
from django.core.exceptions import ValidationError

DF_COLUMNS = ['title', 'datetime', 'link', 'hashtags', 'tweet_id']

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


def parse_tweet(tid, string):

    # Split the tweet into single words 
    raw_text = string.replace("\n", "").split()

    # Store results in dict 
    out = dict(zip(DF_COLUMNS, itertools.repeat(None)))
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
                if out['datetime'] is not None: 
                    raise RuntimeError("Multiple datetimes found")
                out['datetime'] = dt 
                continue 

            except: 
                pass 

            # If that didn't work, try and parse it as a time 
            time = parse_time(f)
            if time: 
                if ('time' in out) and (out['time'] is not None): 
                    raise RuntimeError("Multiple times found")
                out['time'] = time
                continue 

            # If that didn't work, its probably just a hashtag
            hashtags.append(fragment)
            continue

        # No hashtag - could be a website 
        if validate_url(fragment): 
            if out['link'] is not None: 
                raise RuntimeError("Multiple weblinks found")
            out['link'] = fragment
            continue 

        # Anything else; probably raw text from title 
        if not fragment.count('@') and (not finished_title):
            title.append(fragment)

    # If we didn't get a title, datetime and link, give up 
    if not all([title, out['datetime'], out['link']]):
        raise RuntimeError("Could not parse tweet") 

    # Merge the date/hour attributes, if separate 
    if not out['datetime'].hour: 
        time = out.pop('time')
        out['datetime'] = out['datetime'].replace(
            hour=int(time[:2]), minute=int(time[2:]))

    out['title'] = " ".join(title)
    out['hashtags'] = " ".join(hashtags)
    out['tweet_id'] = tid
    return out 