# import os
# import random

# from django.conf import settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE',
# 'airtales.settings')

# import django
# django.setup()
# from airtalesapp.models import User, JournalEntry, Profile, Prompt
# from django.utils.timezone import now
# from django.utils.timezone import timedelta
# from random import randint


# def populate():
#     users_data = [
#         {'email': 'alice@example.com', 'username': 'Alice', 'password': 'password123'},
#         {'email': 'bob@example.com', 'username': 'Bob', 'password': 'password123'},
#         {'email': 'charlie@example.com', 'username': 'Charlie', 'password': 'password123'},
#         {'email': 'felix@example.com', 'username': 'Felix', 'password': 'password123'},
#         {'email': 'lily@example.com', 'username': 'Lily', 'password': 'password123'},
#     ]
    
#     # Load prompts from prompts.txt
#     prompts = []
#     prompts_file_path = os.path.join(settings.BASE_DIR, 'airtalesapp', 'static', 'data', 'prompts.txt')
    
#     if os.path.exists(prompts_file_path):
#         with open(prompts_file_path, 'r') as file:
#             prompts = [line.strip() for line in file.readlines() if line.strip()]
#     else:
#         print(f"Error: The file {prompts_file_path} was not found.")
#         return

#     # Example Glasgow locations for populating entries to show on map
#     glasgow_locations = [
#         {"name": "Glasgow Cathedral", "latitude": 55.8656, "longitude": -4.2378},
#         {"name": "George Square", "latitude": 55.8611, "longitude": -4.2505},
#         {"name": "The University of Glasgow", "latitude": 55.8721, "longitude": -4.2886},
#         {"name": "The Riverside Museum", "latitude": 55.8655, "longitude": -4.3068},
#         {"name": "Hampden Park", "latitude": 55.8259, "longitude": -4.2514},
#         {"name": "Pollok Country Park", "latitude": 55.8231, "longitude": -4.3164},
#     ]

#     # Prepare the users
#     users = []
#     for user_data in users_data:
#         user, created = User.objects.get_or_create(
#             email=user_data['email'],
#             defaults={'username': user_data['username']}
#         )

#         if created:
#             user.set_password(user_data['password'])
#             user.save()

#         users.append(user)

#     # Start from today, create and save prompts
#     today = now().date()
        
#     for i in range(len(prompts)):
#         # Calculate the date for this prompt (starting today and moving forward)
#         prompt_date = today + timedelta(days=i)

#         # Make sure not to add the prompt again if it already exists for that date
#         if not Prompt.objects.filter(date=prompt_date).exists():
#             # Pick a random prompt from the list and assign it to the current date
#             prompt_text = prompts[randint(0, len(prompts) - 1)]

#             # Create the prompt in the database
#             Prompt.objects.get_or_create(
#                 date=prompt_date,
#                 prompt=prompt_text
#             )

#             print(f"Assigned prompt '{prompt_text}' for {prompt_date}.")
    
#     # Create Profile for each user if not exists
#     for user in users:
#         Profile.objects.get_or_create(userID=user)
    
#     # Create sample journal entries for each user
#     for user in users:
#         journal_responses = {
#             'Adventure': ["Today was such an adventure, I walked to the Boyd Orr building.", "Using django has been the greatest adventure of my life"],  # Add responses as needed
#             'Reflect': ["I love reflecting on how much I have learned using django", "Django is so awesome omgggggggg"],
#             # Add more responses for other prompts
#         }

#         prompts = Prompt.objects.all()
#         random_prompt = prompts[random.randint(0, len(prompts) - 1)]
#         prompt_text = random_prompt.prompt
#         if prompt_text in journal_responses:
#             entry_text = random.choice(journal_responses[prompt_text])
#         else:
#             entry_text = "No specific response."

#         # Pick a random location
#         location = random.choice(glasgow_locations)

#         # Create the journal entry
#         JournalEntry.objects.get_or_create(
#             userID=user,
#             date=prompt_date,
#             entry=entry_text,
#             isReported=False,
#             latitude=location['latitude'],
#             longitude=location['longitude'],
#             prompt=random_prompt,
#         )

#     print("Database populated successfully.")

# populate()

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

# 20 sample users
users_data = [
    {'email': f'user{i}@example.com', 'username': f'User{i}', 'password': 'password123'}
    for i in range(1, 21)  # Creates User1, User2, ..., User20
]

# Global capital city coordinates 
capital_cities = [
    {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
    {"name": "Paris", "latitude": 48.8566, "longitude": 2.3522},
    {"name": "Tokyo", "latitude": 35.6895, "longitude": 139.6917},
    {"name": "Cairo", "latitude": 30.0444, "longitude": 31.2357},
    {"name": "Rio de Janeiro", "latitude": -22.9068, "longitude": -43.1729},
    {"name": "Nairobi", "latitude": -1.2864, "longitude": 36.8172},
    {"name": "Sydney", "latitude": -33.8688, "longitude": 151.2093},
    {"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Beijing", "latitude": 39.9042, "longitude": 116.4074},
    {"name": "Mexico City", "latitude": 19.4326, "longitude": -99.1332},
    {"name": "Moscow", "latitude": 55.7558, "longitude": 37.6173},
    {"name": "Dubai", "latitude": 25.276987, "longitude": 55.296249},
    {"name": "Bangkok", "latitude": 13.7563, "longitude": 100.5018},
    {"name": "Buenos Aires", "latitude": -34.6037, "longitude": -58.3816},
    {"name": "Berlin", "latitude": 52.5200, "longitude": 13.4050},
    {"name": "Seoul", "latitude": 37.5665, "longitude": 126.9780},
    {"name": "Lagos", "latitude": 6.5244, "longitude": 3.3792},
    {"name": "Jakarta", "latitude": -6.2088, "longitude": 106.8456},
    {"name": "Toronto", "latitude": 43.65107, "longitude": -79.347015},
    {"name": "Delhi", "latitude": 28.6139, "longitude": 77.2090}
]

def read_prompts_from_file():
    prompts = []
    prompts_file_path = os.path.join(settings.BASE_DIR, 'airtalesapp', 'static', 'data', 'prompts.txt')
    with open(prompts_file_path, 'r') as file:
        prompts = file.readlines()
    # Strip newline characters and return prompts
    return [prompt.strip() for prompt in prompts]

def populate():
    # Create users
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

    # Create profiles for users
    for user in users:
        Profile.objects.get_or_create(userID=user)

    # Get all prompts
    prompts = Prompt.objects.all()
    if not prompts.exists():
        print("Error: No prompts found. Ensure the database is seeded correctly.")
        return
    
    today = now().date()

    # Create journal entries for the next 89 days
    for day in range(89):
        entry_date = today + timedelta(days=day)
        daily_prompt = prompts.filter(date=entry_date).first()

        if not daily_prompt:
            print(f"Skipping {entry_date}: No prompt found.")
            continue

    for user in users:
        # Check if the journal entry already exists for the user on this date
        existing_entry = JournalEntry.objects.filter(userID=user, date=entry_date).first()

        if existing_entry:
            print(f"Skipping entry for {user.username} on {entry_date}: Entry already exists.")
            continue  # Skip creating a new entry if one already exists
        
        location = random.choice(capital_cities)
        num_likes = min(randint(0, 50), len(users))  # Ensure it’s not greater than the number of users
        liked_users = random.sample(users, num_likes)  # Pick random users who liked the post

        journal_entry = JournalEntry.objects.create(
            userID=user,
            date=entry_date,
            entry=f"{user.username}'s thoughts on '{daily_prompt.prompt}'.",
            isReported=False,
            latitude=location["latitude"],
            longitude=location["longitude"],
            prompt=daily_prompt,
        )

        # Add liked users to the entry
        journal_entry.liked_by.set(liked_users)
        journal_entry.save()

        print(f"Created entry for {user.username} on {entry_date}")
            
populate()