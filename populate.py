import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'airtales.settings')

import django
django.setup()
from airtalesapp.models import User, JournalEntry, Profile, Prompt# Reported
from django.utils.timezone import now
from django.utils.timezone import timedelta
from random import randint
def populate():
    users_data = [
     {'email': 'alice@example.com', 'username': 'Alice', 'password': 'password123'},
     {'email': 'bob@example.com', 'username': 'Bob', 'password': 'password123'},
     {'email': 'charlie@example.com', 'username': 'Charlie', 'password': 'password123'},
    ]
    prompt_data = [
     {'date': now().date()- timedelta(days=3), 'prompt':'tempting'},
     {'date': now().date()- timedelta(days=2), 'prompt':'beauty'},
     {'date': now().date()- timedelta(days=1), 'prompt':'ageing'},
    ]

    users = []
    for user_data in users_data:
        user = User.objects.create_user(email=user_data['email'], username=user_data['username'], password=user_data['password'])
        #user = User.objects.get_or_create(email=user_data['email'], username=user_data['username'], password=user_data['password'])
        users.append(user)

    for user in users:
        for i in range(1,3): 
            date = now().date() - timedelta(days=randint(1, 10))
            entry_text = f"Entry from {user.username} on {date}: Today was an amazing day!"
            JournalEntry.objects.create(userID=user, date=date, entry=entry_text, isReported=False)


    for user in users:
        Profile.objects.create(userID=user, date=now().date())


populate()