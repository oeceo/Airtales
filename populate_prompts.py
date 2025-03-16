import os
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airtales.settings')

import django
django.setup()

from airtalesapp.models import Prompt
from datetime import date, timedelta

# Path to the prompts.txt file
prompts_file_path = os.path.join(settings.BASE_DIR, 'airtalesapp/static/data/prompts.txt')

def populate_prompts():
    try:
        with open(prompts_file_path, 'r') as file:
            prompts = file.readlines()
    except FileNotFoundError:
        print(f"Error: {prompts_file_path} not found. Ensure the file exists.")
        return
    
    if not prompts:
        print("Error: No prompts found in the file.")
        return
    
    today = date.today()

    # Add each prompt for the next 89 days
    for i, prompt_text in enumerate(prompts):
        prompt_date = today + timedelta(days=i)
        prompt_text = prompt_text.strip()  # Clean up any extra whitespace or newline
       
        # Creates a new Prompt entry in the database
        Prompt.objects.create(date=prompt_date, prompt=prompt_text)
    
    print(f"Successfully populated {len(prompts)} prompts.")


populate_prompts()