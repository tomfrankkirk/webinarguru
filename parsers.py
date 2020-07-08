import re 
import dateutil
from urllib.parse import urlparse
from urllib.parse import urlparse
from dateutil.parser import parse as parse_datetime

from django.forms import URLField
from django.core.exceptions import ValidationError

def parse_time(string):

    time = None 
    
    time_digits = re.findall(r'\d', string)
    if len(time_digits) == 4: 
        time = "".join(time_digits)

    elif string.count('am') or string.count('pm'): 
        time = re.match(r'\d*(am)?(pm)?', string).group()
            
    elif re.match(r'\d*[\.\:\sh]{1}(\d)?', string):
        time = re.match(r'\d*[\.\:\sh]{1}(\d)?', string).group()

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


def parse_tweet(string):

    out = {}
    hashtags = []

    raw_text = string.strip(" \n")
    raw_text = raw_text.replace("\n", "").split()
    for fragment in raw_text: 
        if fragment.count("#"):
            f = fragment.strip("#")

            # Try and parse as a combined datetime first 
            try: 
                dt = parse_datetime(f, fuzzy=True)
                if (dt.hour != 0) or (dt.minute != 0): 
                    raise RuntimeError("haven't checked this code yet")
                    time = (100 * dt.hour) + dt.minute
                    assert 'time' not in out 
                    out['time'] = f"{time:04d}"

                assert 'datetime' not in out 
                out['datetime'] = dt 
                continue 

            except: 
                pass 

            # If that didn't work, try and parse it as a time 
            time = parse_time(f)
            if time: 
                assert 'time' not in out 
                out['time'] = time 
                continue 

            # If that didn't work, its probably just a hashtag
            hashtags.append(fragment)
            continue

        # No hashtag - could be a website 
        if validate_url(fragment): 
            assert 'link' not in out 
            out['link'] = fragment
            continue 

        # print("Did not process", fragment)
        
    out['hashtags'] = hashtags
    return out 