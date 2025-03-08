from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import JournalEntry
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.utils.timezone import timedelta
from .models import Prompt 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

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

# def journal_entry(request):
#     if request.method == "POST":
#         # journal_text= request.POST.get("journa_text")
#         # if entry_text: 
#         #     JournalEntry.objects.create(userID=request.user, date=now().date(), entry=entry_text)
#         #     # JournalEntry.objects.create(userID=user, date=date, entry=entry_text, isReported=False)
#         #    # return redirect("success_page")
#         # return redirect("/profile/")   
#     return render(request, "profile.html")

@login_required
def profile(request):
    #this returns the days prompt to the profile
    today = now().date()  # Get today's date
    prompt_text = "No prompt available for today."  # default if there is no prompt
    try:
        prompt = Prompt.objects.get(date=today)#get the prompt for the day
        prompt_text = prompt.prompt  
    except Prompt.DoesNotExist:
        pass  
    #this checks if the user has already made a journal entry
    prior_entry = JournalEntry.objects.filter(userID=request.user, date=today).exists()

    #gets the previous journal entries
    previous_entries = JournalEntry.objects.filter(userID=request.user).exclude(date=today).order_by('-date')
    context = {
        'prompt_text': prompt_text,
        'prior_entry':prior_entry,  
        'journal_entries':previous_entries
    }
    return render(request, 'profile.html', context)

def view_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id)
    return render(request, 'view_entry.html', {'entry': entry})

def userjournal(request):
    return render(request, 'userjournal.html')