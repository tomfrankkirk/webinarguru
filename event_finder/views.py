from datetime import date
from itertools import repeat
from django.forms.formsets import all_valid
from django.shortcuts import render
from django.http import HttpResponse
import json 
import ics
import datetime

from .models import Event
from .db_updates import time_now

# Create your views here.
def index(request):
    cutoff = time_now() + datetime.timedelta(weeks=4)
    all_events = Event.objects.filter(datetime__lte=cutoff).order_by('datetime')
    date_events = {}
    for e in all_events:
        dt = e.datetime.strftime('%a, %d %b %Y')
        if dt not in date_events: 
            date_events[dt] = [e]
        else: 
            date_events[dt].append(e)

    context = {
        'date_events': date_events
    }
    return render(request, 'event_finder/index.html', context)

def detail(request, id):
    event = Event.objects.get(tweet_id=id)
    c = ics.Calendar()
    e = ics.Event()
    e.name = event.title
    e.begin = event.datetime.strftime("%Y-%m-%d %H:%M")
    end = event.datetime + datetime.timedelta(hours=1)
    e.end = end.strftime("%Y-%m-%d %H:%M")
    e.url = event.link 
    c.events.add(e)

    response = HttpResponse(str(c), content_type="application/ics")
    response['Content-Disposition'] = 'inline; filename=%s.ics' % e.name
    return response
