import time
import pickle 

import pandas as pd 
import tweepy
import pygsheets

from tokens import oauth_tokens, accesss_tokens
import parsers

def construct_sheet(df, tweets):
    if df.empty:
        df = pd.DataFrame(columns=parsers.DF_COLUMNS)

    for tid, tweet_string in tweets:
        if tid not in df['tweet_id'].values:
            try: 
                t = parsers.parse_tweet(tid, tweet_string)
                df = df.append(t, ignore_index=True)
            except RuntimeError as e: 
                print(f"Skipped: {tweet_string}")
                pass 
            except Exception as e: 
                raise e
    return df 

if __name__ == '__main__':

    gc = pygsheets.authorize(service_file='tkirk_key.json')
    sh = gc.open('production')
    wks = sh[0]

    auth = tweepy.OAuthHandler(*oauth_tokens)
    auth.set_access_token(*accesss_tokens)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.me()
    mentions = api.mentions_timeline(tweet_mode='extended')

    to_parse = zip([t.id for t in mentions], [t.full_text for t in mentions])
    df = construct_sheet(wks.get_as_df(), to_parse)
    wks.set_dataframe(df,(1,1))
    sh.update_properties()
    print(df)