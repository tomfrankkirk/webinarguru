import itertools

from django.test import TestCase

from event_finder.twitter_api import parsers
from event_finder.models import Event

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
    #Nov7th
    #7pm
    #testtalkwebinar
    clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Test Talk 
    #07-Dec-2020
    #19h00
    #thisisafuntalk
    www.clickthislink.org 
    @WebinarG #SpreadTheWord""",

    """We are holding a Theatre extravangza
    #10/11
    #1900
    #Testtalk
    https://clickthislink.co.uk 
    @WebinarG #SpreadTheWord""",

    """We are holding a Theatre extravangza
    #14-Oct
    #19:00hrs
    #Testtalk
    clickthislink.co.uk 
    @WebinarG #SpreadTheWord""",

    """We are holding a Webinar
    #20/12/20
    #19.00
    #testtalkwebinar
    clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Webinar
    #Nov-12
    #19h
    #testtalkwebinar
    www.clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Webinar
    #Dec-11
    #19,00
    #testtalkwebinar
    www.clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Webinar
    #10.11.20
    #1900BST
    #testtalkwebinar
    www.clickthislink.co.uk 
    @webinarguru #spreadtheword""",

    """We are holding a Webinar
    #11/Nov/20
    #1900GMT
    #testtalkwebinar
    www.clickthislink.co.uk 
    @webinarguru #spreadtheword"""

])
