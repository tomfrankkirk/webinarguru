import parsers
import pandas as pd 
import pygsheets
import gspread

gc = pygsheets.authorize(service_file='creds.json')



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

TWEETS = [

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
    @webinarguru #spreadtheword"""

    

]

def test_times():
    for target, timestring in TIMES: 
        assert parsers.parse_time(timestring) == target

def test_tweets(): 
    for tweet in reversed(TWEETS):
        parsed = parsers.parse_tweet(tweet)
        print(parsed)

def construct_sheet():
    df = pd.DataFrame(columns=parsers.DF_COLUMNS)
    for tweet in TWEETS:
        t = parsers.parse_tweet(tweet)
        df = df.append(t, ignore_index=True)
    sh=gc.open('Tutorial')
    wks =sh[0]
    wks.set_dataframe(df,(1,1))

    print(df)
    

if __name__ == "__main__":
    construct_sheet()
