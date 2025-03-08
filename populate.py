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
     {'date': now().date()- timedelta(days=2), 'prompt':'tempting'},
     {'date': now().date()- timedelta(days=1), 'prompt':'beauty'},
     {'date': now().date()- timedelta(days=0), 'prompt':'ageing'},
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
            JournalEntry.objects.get_or_create(userID=user, date=date, entry=entry_text, isReported=False)

    for prompt_entry in prompt_data:
        date=prompt_entry['date']
        prompt_add = prompt_entry['prompt']
        Prompt.objects.get_or_create(date= date, prompt=prompt_add)


    for user in users:
        Profile.objects.get_or_create(userID=user)


populate()