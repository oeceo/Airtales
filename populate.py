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
        {'email': 'felix@example.com', 'username': 'Felix', 'password': 'password123'},
        {'email': 'lily@example.com', 'username': 'Lily', 'password': 'password123'},
    ]
    prompt_data = [
     {'date': now().date()- timedelta(days=4), 'prompt':'ageing'},
     {'date': now().date()- timedelta(days=3), 'prompt':'conflict'},
     {'date': now().date()- timedelta(days=2), 'prompt':'tempting'},
     {'date': now().date()- timedelta(days=1), 'prompt':'beauty'},
     {'date': now().date()- timedelta(days=0), 'prompt':'paradise'},
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

    # Create prompts
    for prompt_entry in prompt_data:
        date = prompt_entry['date']
        prompt_add = prompt_entry['prompt']
        Prompt.objects.get_or_create(date= date, prompt=prompt_add)

    # Generic responses to specific prompts
    journal_responses = {
        'ageing': [
            "In a society obsessed with youth, ageing is often feared or ignored. But I'm starting to embrace it as a process of transformation, where each year adds layers of wisdom and understanding. It's not about holding onto the past but stepping into the future with confidence.",
            "As I grow older, I'm realizing that ageing isn't just about getting wrinkles or grey hair. It's about changing priorities, letting go of things that no longer serve me, and finding comfort in the quiet moments that I once overlooked.",
            "The process of ageing is like the slow turning of a page in a book. At times, it feels melancholic, but it's also a blessing. It allows us to reflect, to cherish experiences, and to find beauty in the years lived, no matter how many they may be.",
            "Getting older is weird. I swear I'm 25 in my head, but my knees tell a different story. I guess it's just a reminder that time waits for no one. Oh well, I'll take the wisdom with the wrinkles!",
            "Ageing isn't as scary as I thought. Sure, I'm getting more tired, but I'm also more comfortable with myself. I know what I want now, and I'm not afraid to go for it.",
        ],

        'conflict': [
            "When I'm in conflict with someone, I used to shut down. But now, I try to sit with the discomfort, because I know it means something needs to change. It's hard, but through conflict, I'm learning to communicate better and understand where others are coming from.",
            "Conflict today feels different. We live in a time where divisiveness often feels overwhelming, but there's hope in the potential for dialogue. True conflict resolution doesn't lie in silencing differences, but in engaging with empathy and finding common ground despite our disagreements.",
            "Conflict is often viewed as a negative force, but I see it as a challenge that pushes us to confront uncomfortable truths. It tests our values, our relationships, and our ability to communicate, ultimately shaping who we are as individuals and as a society.",
            "I'm not good with conflict. I'll either avoid it completely or just get so awkward that the other person feels bad for me. Either way, it's usually messy. But hey, at least I try to learn from it.",
            "Conflict? Oh, I try to avoid it, to be honest. But sometimes, it just happens, and then it's like, 'Well, here we are.' I try to make peace quickly, though — no need to drag things out.",
        ],

        'tempting': [
            "In today's fast-paced world, temptation often takes the form of instant gratification — from social media validation to consumerism. But I'm learning to slow down, to question what I truly need versus what's just tempting in the moment. The act of pausing is becoming more powerful.",
            "Life is full of temptations, but I've learned to see them as opportunities to strengthen my resolve. What's tempting isn't always what's best, and the hardest decisions often lead to the most meaningful growth.",
            "I'm constantly tempted by the easy way out — whether it's skipping a workout or mindlessly scrolling through my phone. But I'm starting to realize that the real reward comes when I resist temptation and choose the things that truly matter to me in the long run.",
            "It's so tempting to skip the gym today. My couch is calling me like it's a long-lost friend. But I know I'll feel guilty later if I don't go. I'm not giving in. Today, I'll be strong.",
            "I had a slice of cake, even though I said I wouldn't. It was tempting, and honestly, I'm not mad about it. Sometimes you just have to go with the flow, right?",
        ],

        'beauty': [
            "I used to think beauty was all about appearances, but I've started seeing it differently. It's in the way someone makes you feel, the way kindness radiates from a person's actions. Beauty is in the energy we put into the world and the connections we make.",
            "As beauty standards become more diverse, I see the conversation around beauty evolving. It's less about conforming to a specific look and more about embracing differences. True beauty is no longer confined to one ideal but exists in the vast spectrum of human expression.",
            "We've often been told that beauty is something to be pursued, but I've realized it's something to be experienced. It's in the quiet moments of joy, the acts of kindness, and the love we give — all of which are invisible yet deeply felt. Beauty is what we make of it.",
            "I saw someone today and thought, 'Wow, they're gorgeous.' Then I realized they were just wearing a really cool jacket. I guess beauty's all about the vibe, not just the looks.",
            "Sometimes beauty is just about feeling good. It's not about how you look; it's about how you carry yourself. Still, a good skincare routine helps, too.",
        ],

        'paradise': [
            "Paradise isn't a destination; it's a state of mind. It's the ability to find joy and contentment in the present moment, despite all the challenges.",
            "I used to think of paradise as a far-off, ideal place. But now, I believe it's about being present in the moment, savoring life's simple pleasures.",
            "Paradise seems like a distant, unattainable dream, but I'm beginning to see that it's not about physical perfection but emotional and mental peace. It's about finding balance, reconnecting with nature, and living in harmony with the world around us, even in a chaotic society.",
            "If paradise is a place, then mine is anywhere with a comfy chair and snacks. Seriously, that's my dream vacation — no crowds, no schedules, just good food and relaxation.",
            "I keep daydreaming about a beach somewhere, but then I remember I can't swim. Maybe paradise isn't about the place but just getting away from work for a bit. A quiet day sounds nice.",
        ],
    }

    # Create entries for each user based on each prompt
    for user in users:
        for prompt_entry in prompt_data:
            #date = now().date() #- timedelta(days=randint(1, 10))
            #date = now().date()-timedelta(days=i)
            date = prompt_entry['date']
            prompt = Prompt.objects.filter(date=date).first() #first() returns null if no prompt found
            prompt_text = prompt.prompt if prompt else "No entry."
            
            if prompt_text in journal_responses:
                entry_index = prompt_data.index(prompt_entry)
                entry_text = journal_responses[prompt_text][entry_index]
            
            #entry_text = f"Entry from {user.username} on {date}: Today was an amazing day!"
            JournalEntry.objects.get_or_create(
                userID=user, 
                date=date, 
                entry=entry_text, 
                isReported=False
            )
            
    for user in users:
        Profile.objects.get_or_create(userID=user)

populate()