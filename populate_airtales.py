import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'airtales.settings') 
import django
django.setup()

from airtalesapp.models import User, JournalEntry, Profile, Prompt
from django.utils.timezone import now
from django.utils.timezone import timedelta
from random import randint
# def populate():
users_data = [
     {'email': 'alice@example.com', 'username': 'Alice', 'password': 'password123'},
     {'email': 'bob@example.com', 'username': 'Bob', 'password': 'password123'},
     {'email': 'charlie@example.com', 'username': 'Charlie', 'password': 'password123'},
    ]

users = []
for user_data in users_data:
    user = User.objects.create_user(email=user_data['email'], username=user_data['username'], password=user_data['password'])
    users.append(user)

# Generate prompts for the last 10 days
prompts = []
for i in range(10):
    date = now().date() - timedelta(days=i)
    prompt_text = f"Prompt for {date}: Describe your perfect day!"
    prompt = Prompt.objects.create(date=date, prompt=prompt_text)
    prompts.append(prompt)

Generate journal entries for each user
for user in users:
    for i in range(randint(3, 7)):  # Each user gets 3 to 7 journal entries
        date = now().date() - timedelta(days=randint(1, 10))
        entry_text = f"Entry from {user.username} on {date}: Today was an amazing day!"
        JournalEntry.objects.create(userID=user, date=date, entry_text=entry_text, isReported=False)

Create profiles for each user
for user in users:
    Profile.objects.create(userID=user, date=now().date())

print("✅ Database successfully populated!")