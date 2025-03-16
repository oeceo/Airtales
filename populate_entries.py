import os
import django
import datetime
import random 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airtales.settings')


django.setup()

# Now you can import your models
from airtalesapp.models import User, JournalEntry, Prompt



# List of capital cities with their corresponding latitude and longitude
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

def populate_entries():
    users = User.objects.all()  # Assuming you're populating for all users
    prompts = Prompt.objects.all()

    for user in users:
        for day_offset in range(1, 90):  # Generate for 89 days
            date = datetime.date.today() + datetime.timedelta(days=day_offset)

            # Check if an entry already exists for this user on the given date
            if not JournalEntry.objects.filter(userID=user, date=date).exists():
                # Pick a random prompt
                daily_prompt = random.choice(prompts)

                # Choose a random city to assign
                city_name, (lat, lon) = random.choice(list(capital_cities.items()))

                # Define location using lat and lon
                location = {"latitude": lat, "longitude": lon}

                # Define liked_users (for now, you can leave it empty or add some users)
                liked_users = []  # Or populate with some actual users

                # Create the journal entry
                journal_entry = JournalEntry.objects.create(
                    userID=user,
                    date=date,  # Use date instead of entry_date
                    entry=f"I have such amazing insightful thoughts on '{daily_prompt.prompt}'.",
                    isReported=False,
                    latitude=location["latitude"],
                    longitude=location["longitude"],
                    prompt=daily_prompt,
                )

                # Add liked users to the entry (many-to-many relationship)
                journal_entry.liked_by.set(liked_users)

                # Save the entry to commit changes to the database
                journal_entry.save()

if __name__ == "__main__":
    populate_entries()