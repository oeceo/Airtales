import os
import random

from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'airtales.settings')

import django
django.setup()
from airtalesapp.models import User, JournalEntry, Profile, Prompt
from django.utils.timezone import now
from django.utils.timezone import timedelta
from random import randint


def populate():
    users_data = [
        {'email': 'alice@example.com', 'username': 'Alice', 'password': 'password123'},
        {'email': 'bob@example.com', 'username': 'Bob', 'password': 'password123'},
        {'email': 'charlie@example.com', 'username': 'Charlie', 'password': 'password123'},
        {'email': 'felix@example.com', 'username': 'Felix', 'password': 'password123'},
        {'email': 'lily@example.com', 'username': 'Lily', 'password': 'password123'},
    ]
    
    # Load prompts from prompts.txt
    prompts = []
    prompts_file_path = os.path.join(settings.BASE_DIR, 'airtalesapp', 'static', 'data', 'prompts.txt')
    
    if os.path.exists(prompts_file_path):
        with open(prompts_file_path, 'r') as file:
            prompts = [line.strip() for line in file.readlines() if line.strip()]
    else:
        print(f"Error: The file {prompts_file_path} was not found.")
        return

    # Example Glasgow locations for populating entries to show on map
    glasgow_locations = [
        {"name": "Glasgow Cathedral", "latitude": 55.8656, "longitude": -4.2378},
        {"name": "George Square", "latitude": 55.8611, "longitude": -4.2505},
        {"name": "The University of Glasgow", "latitude": 55.8721, "longitude": -4.2886},
        {"name": "The Riverside Museum", "latitude": 55.8655, "longitude": -4.3068},
        {"name": "Hampden Park", "latitude": 55.8259, "longitude": -4.2514},
        {"name": "Pollok Country Park", "latitude": 55.8231, "longitude": -4.3164},
    ]

    # Prepare the users
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={'username': user_data['username']}
        )

        if created:
            user.set_password(user_data['password'])
            user.save()

        users.append(user)

    # Start from today, create and save prompts
    day = now().date() - timedelta(days=3)
        
    for i in range(len(prompts)):
        # Calculate the date for this prompt (starting today and moving forward)
        prompt_date = day + timedelta(days=i)

        # Make sure not to add the prompt again if it already exists for that date
        if not Prompt.objects.filter(date=prompt_date).exists():
            # Pick a random prompt from the list and assign it to the current date
            prompt_text = prompts[randint(0, len(prompts) - 1)]

            # Create the prompt in the database
            Prompt.objects.get_or_create(
                date=prompt_date,
                prompt=prompt_text
            )

            print(f"Assigned prompt '{prompt_text}' for {prompt_date}.")
    
    # Create Profile for each user if not exists
    for user in users:
        Profile.objects.get_or_create(userID=user)
    
    # Create sample journal entries for each user
    for user in users:
        journal_responses = {
            'Adventure': ["Today was such an adventure, I walked to the Boyd Orr building.", "Using django has been the greatest adventure of my life"],  # Add responses as needed
            'Reflect': ["I love reflecting on how much I have learned using django", "Django is so awesome omgggggggg"],
            # Add more responses for other prompts
        }

        prompts = Prompt.objects.all()
        random_prompt = prompts[random.randint(0, len(prompts) - 1)]
        prompt_text = random_prompt.prompt
        if prompt_text in journal_responses:
            entry_text = random.choice(journal_responses[prompt_text])
        else:
            entry_text = "No specific response."

        # Pick a random location
        location = random.choice(glasgow_locations)

        # Create the journal entry
        JournalEntry.objects.get_or_create(
            userID=user,
            date=prompt_date,
            entry=entry_text,
            isReported=False,
            latitude=location['latitude'],
            longitude=location['longitude'],
            prompt=random_prompt,
        )

    print("Database populated successfully.")


populate()