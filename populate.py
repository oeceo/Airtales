import os
import random
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
     {'date': now().date()- timedelta(days=2), 'prompt':'tempting'},
     {'date': now().date()- timedelta(days=1), 'prompt':'beauty'},
     {'date': now().date()- timedelta(days=0), 'prompt':'ageing'},
    ]
    # Example Glasgow locations for populating entries to show on map
    glasgow_locations = [
    {"name": "Glasgow Cathedral", "latitude": 55.8656, "longitude": -4.2378},
    {"name": "George Square", "latitude": 55.8611, "longitude": -4.2505},
    {"name": "The University of Glasgow", "latitude": 55.8721, "longitude": -4.2886},
    {"name": "The Riverside Museum", "latitude": 55.8655, "longitude": -4.3068},
    {"name": "Hampden Park", "latitude": 55.8259, "longitude": -4.2514},
    {"name": "Pollok Country Park", "latitude": 55.8231, "longitude": -4.3164},
]

    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'], 
            defaults={'username': user_data['username']}
        )

        if created:
            user.set_password(user_data['password'])
            user.save()
        
        
        # user = User.objects.get_or_create_user(email=user_data['email'], username=user_data['username'], password=user_data['password'])
        
        users.append(user)

    for user in users:
        for i in range(0,2): 
            #date = now().date() #- timedelta(days=randint(1, 10))
            date = now().date()-timedelta(days=i)
            entry_text = f"Entry from {user.username} on {date}: Today was an amazing day!"
            
            location = random.choice(glasgow_locations)
        
            JournalEntry.objects.get_or_create(
            userID=user,
            date=date,
            entry=entry_text,
            isReported=False,
            defaults={
                'latitude': location['latitude'],
                'longitude': location['longitude'],
            }
        )

    for prompt_entry in prompt_data:
        date=prompt_entry['date']
        prompt_add = prompt_entry['prompt']
        Prompt.objects.get_or_create(date= date, prompt=prompt_add)


    for user in users:
        Profile.objects.get_or_create(userID=user)


populate()