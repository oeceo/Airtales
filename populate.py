import os
import random
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'airtales.settings')

import django
django.setup()
from airtalesapp.models import User, JournalEntry, Profile, Prompt
from django.utils.timezone import timedelta, now

# 20 sample users
users_data = [
    {'email': f'user{i}@example.com', 'username': f'User{i}', 'password': 'password123'}
    for i in range(1, 21)  # Creates User1, User2, ..., User20
]

# Global capital city coordinates 
capital_cities = {
    "Washington, D.C.": (38.9072, -77.0369),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6762, 139.6503),
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Madrid": (40.4168, -3.7038),
    "Rome": (41.9028, 12.4964),
    "Ottawa": (45.4215, -75.6992),
    "Canberra": (-35.2809, 149.1300),
    "Beijing": (39.9042, 116.4074),
    "New Delhi": (28.6139, 77.2090),
    "Moscow": (55.7558, 37.6173),
    "Brasília": (-15.7801, -47.9292),
    "Buenos Aires": (-34.6037, -58.3816),
    "Cairo": (30.0444, 31.2357),
    "Seoul": (37.5665, 126.9780),
    "Mexico City": (19.4326, -99.1332),
    "Amsterdam": (52.3676, 4.9041),
    "Prague": (50.0755, 14.4378),
    "Athens": (37.9838, 23.7275),
    "Bangkok": (13.7563, 100.5018),
    "Stockholm": (59.3293, 18.0686),
    "Helsinki": (60.1692, 24.9402),
    "Oslo": (59.9139, 10.7522),
    "Vienna": (48.2082, 16.3738),
    "Warsaw": (52.2298, 21.0118),
    "Copenhagen": (55.6761, 12.5683),
    "Bern": (46.9481, 7.4474),
    "Riyadh": (24.7136, 46.6753),
    "Dubai": (25.276987, 55.296249),
    "Singapore": (1.3521, 103.8198)
}

def read_prompts_from_file():
    prompts = []
    prompts_file_path = os.path.join(settings.BASE_DIR, 'airtalesapp', 'static', 'data', 'prompts.txt')
    with open(prompts_file_path, 'r') as file:
        prompts = file.readlines()
    # Strip newline characters and return prompts
    return [prompt.strip() for prompt in prompts]


def populate_users():
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
        
    print(f"Successfully populated {len(users)} users.")
            
            
def populate_prompts():
    prompts = read_prompts_from_file()
    if not prompts:
        print("Error: No prompts found in the file.")
        return
    
    # Add each prompt for the next 89 days
    for i, prompt_text in enumerate(prompts):
        prompt_date = now() + timedelta(days=i)-timedelta(days=4)
        prompt_text = prompt_text.strip()  # Clean up any extra whitespace or newline

        # Creates a new Prompt entry in the database
        Prompt.objects.create(date=prompt_date, prompt=prompt_text)
    
    print(f"Successfully populated {len(prompts)} prompts.")
            
            
def populate_entries():
    users = User.objects.all()
    prompts = Prompt.objects.all()

    for user in users:
        for prompt in prompts:  # Generate an entry for each prompt
            # Check if an entry already exists for this user on the given date
            if not JournalEntry.objects.filter(userID=user, date=prompt.date).exists():
                # Choose a random city to assign
                _, (lat, lon) = random.choice(list(capital_cities.items()))

                # Define location using lat and lon
                location = {"latitude": lat, "longitude": lon}

                # Define liked_users
                num_likes = min(random.randint(0, 50), len(users))  # Ensure it’s not greater than the number of users
                liked_users = random.sample(list(users), num_likes)  # Pick random users who liked the entry

                # Create the journal entry
                journal_entry = JournalEntry.objects.create(
                    userID=user,
                    date=prompt.date,
                    entry=f"I have such amazing insightful thoughts on '{prompt.prompt}'.",
                    isReported=False,
                    latitude=location["latitude"],
                    longitude=location["longitude"],
                    prompt=prompt,
                )

                # Add liked users to the entry (many-to-many relationship)
                journal_entry.liked_by.set(liked_users)

                # Save the entry to commit changes to the database
                journal_entry.save()
                
    print(f"Successfully added journal entries for {len(users)} users and {len(prompts)} prompts.")
            
populate_users()
populate_prompts()
populate_entries()
