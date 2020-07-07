import time
import pickle 
import datetime 
import dateutil 
from dateutil.parser import parse as parse_datetime

from parsers import parse_time, parse_url

import tweepy
from tokens import oauth_tokens, accesss_tokens

def extract_webinar_info(status):

    out = {}
    hashtags = []

    raw_text = status.full_text.strip(" \n")
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
            time = parse_time(fragment)
            if time: 
                assert 'time' not in out 
                out['time'] = time 
                continue 

            # If that didn't work, its probably just a hashtag
            hashtags.append(fragment)
            continue

        # No hashtag - could be a website 
        url = parse_url(fragment)
        if url: 
            assert 'link' not in out 
            out['link'] = url
            continue 

        print("Did not process", fragment)
        
    out['hashtags'] = hashtags

    print("Processed output", out)
    return out 

if __name__ == '__main__':

    auth = tweepy.OAuthHandler(*oauth_tokens)
    auth.set_access_token(*accesss_tokens)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.me()

    # mentions = api.mentions_timeline(tweet_mode='extended')
    with open('dummy.pkl', 'rb') as f: 
        mentions = [ pickle.load(f) ]

    for mention in reversed(mentions):
        print(str(mention.user.name))
        print(mention.full_text)
        print("")
        if mention.user.name == 'Rob Staruch':
            extract_webinar_info(mention)

