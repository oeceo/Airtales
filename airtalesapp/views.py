from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import JournalEntry
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.utils.timezone import timedelta
from .models import Prompt 

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def explore(request):
    return render(request, 'explore.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def profile(request):
    today = now().date()  # Get today's date
    prompt_text = "No prompt available for today."  # Default if no prompt exists
    try:
        #prompt = Prompt.objects.get(date=today- timedelta(days=1))
        prompt = Prompt.objects.get(date=today)
        prompt_text = prompt.prompt  
    except Prompt.DoesNotExist:
        pass  

    context = {
        'prompt_text': prompt_text,  
    }
    return render(request, 'profile.html', context)

def userjournal(request):
    return render(request, 'userjournal.html')