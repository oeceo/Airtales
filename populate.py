import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'AirTales.settings')

import django
django.setup()
from airtalesapp.models import User, JournalEntry, Profile, Prompt, Reported
from django.utils.timezone import now
from django.utils.timezone import timedelta
from random import randint
def populate():

