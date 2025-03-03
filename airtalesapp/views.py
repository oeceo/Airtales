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

def save_entry(request):
    if request.method == "POST":
        entry_text= request.POST.get("entry_text")
        if entry_text: 
            JournalEntry.objects.create(userID=request.user, date=now().date(), entry=entry_text)
            # JournalEntry.objects.create(userID=user, date=date, entry=entry_text, isReported=False)
           # return redirect("success_page")
        return redirect("/profile/")   
    return render(request, "profile.html")

def profile(request):
    #this returns the days prompt to the profile
    today = now().date()  # Get today's date
    prompt_text = "No prompt available for today."  # default if there is no prompt
    try:
        prompt = Prompt.objects.get(date=today)#get the prompt for the day
        prompt_text = prompt.prompt  
    except Prompt.DoesNotExist:
        pass  

    context = {
        'prompt_text': prompt_text,  
    }
    return render(request, 'profile.html', context)

def userjournal(request):
    return render(request, 'userjournal.html')