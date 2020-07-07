import re 
import dateutil
from urllib.parse import urlparse
from urllib.parse import urlparse


def parse_time(string):

    time = None 
    
    time_digits = re.findall(r'\d', string)
    if len(time_digits) == 4: 
        time = "".join(time_digits)

    elif string.count('am') or string.count('pm'): 
        time = re.match(r'\d*(am)?(pm)?', string).group()
            
    elif re.match(r'\d*[\.\:\sh]\d', string):
        time = re.match(r'\d*[\.\:\sh]\d', string)

    if time: 
        time = int("".join(re.findall('\d', time)))
        if time < 100: time *= 100
        if string.count('pm') and (time < 1159): time += 1200 
        return f"{time:04d}"

    else: 
        return None 


def parse_url(string): 
    min_attributes = ('scheme', 'netloc', 'path')
    tokens = urlparse(string)
    if sum([ bool(getattr(tokens, qualifying_attr)) 
        for qualifying_attr in min_attributes ]) > 1:
        return string
    else: 
        return None 
