import parsers
import itertools
import dateparser

import pygsheets
import pandas as pd 

from mentions import construct_sheet

TIMES = [
    ('1245', '1245'),
    ('1245', '12:45'),
    ('1245', '12h45'),
    ('1245', '12.45pm'),
    ('1245', '12.45'),
    ('1245', '12 45'),
    ('1500', '3pm'), 
    ('0700', '7am')
]

DATES = [
    '3rd July',
    '03/07',
    '3 July'
    '3-Jul'
]

DATE_TIMES = [

]

TWEETS = zip(itertools.count(), [

    """We are holding a Webinar
    #July7th
    #7pm
    #testtalkwebinar
    clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Test Talk 
    #07-jul-2020
    #19h00
    #thisisafuntalk
    www.clickthislink.org 
    @WebinarG #SpreadTheWord""",

    """We are holding a Theatre extravangza
    #7/7
    #1900
    #Testtalk
    https://clickthislink.co.uk 
    @WebinarG #SpreadTheWord""",

    """We are holding a Theatre extravangza
    #July7th
    #19:00hrs
    #Testtalk
    clickthislink.co.uk 
    @WebinarG #SpreadTheWord""",

    """We are holding a Webinar
    #07/07/20
    #19.00
    #testtalkwebinar
    clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Webinar
    #Jul-7
    #19h
    #testtalkwebinar
    www.clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Webinar
    #Jul-7
    #19,00
    #testtalkwebinar
    www.clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Webinar
    #7.7.20
    #1900BST
    #testtalkwebinar
    www.clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Webinar
    #07/07/20
    #1900GMT
    #testtalkwebinar
    www.clickthislink.co.uk 
    @webinarguru #spreadtheword"""

])

def test_times():
    for target, timestring in TIMES: 
        assert parsers.parse_time(timestring) == target

def test_tweets(): 
    for tweet in reversed(TWEETS):
        parsed = parsers.parse_tweet(tweet)
        print(parsed)

def test_sheet():
    gc = pygsheets.authorize(service_file='tkirk_key.json')
    sh = gc.open('testing')
    wks = sh[0]
    df = construct_sheet(wks.get_as_df(), TWEETS)
    wks.set_dataframe(df,(1,1))
    print(df)
    

def new_parsetime():
    string = "Doesn't get much better than this! Our next Webinar on Acute Burns Monday 27th of July 20:00 (GMT) is open for registration. Definitely not one to miss. #SpreadTheWord @WebinarG @PlasticsFella @PLASTAUK @BritishBurn @plasticstrainee  https://t.co/BbzBtkw4Df"
    fragments = string.split()

    for substring in [ fragments[x:y] for x,y in itertools.combinations(range(len(fragments)+1), 2)]:
        try: 
            joined = " ".join(substring)
            dt = dateparser.parse(joined)
            if dt is not None: 
                print(dt)
        except: 
            pass 

if __name__ == "__main__":
    test_sheet()
