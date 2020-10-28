"""webinarguru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from itertools import repeat
import background_task
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path

import event_finder
from background_task import background
from event_finder.worker import (background_load_events_to_db, 
    background_load_dummy_events_to_db)

urlpatterns = [ 
    path('event_finder/', include('event_finder.urls')),
    path('admin/', admin.site.urls),
    path('', event_finder.views.index)
    # re_path(r'.*', views.index)
]

# background_load_dummy_events_to_db(repeat=10, repeat_until=None)
# background_load_events_to_db(repeat=3600, repeat_until=None)

# TODO: hide the secrets off git