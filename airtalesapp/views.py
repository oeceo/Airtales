from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from .models import JournalEntry
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.utils.timezone import timedelta
from .models import Prompt 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404


def index(request):
    
    today = todays_date()
    yesterday = yesterdays_date()

    current_prompt_text = get_prompt(today)
    yesterdays_prompt_text = get_prompt(yesterday)

    todays_entries = JournalEntry.objects.filter(date=today)
    yesterdays_entries = JournalEntry.objects.filter(date=yesterday)

    current_post_position1 = 0
    current_post_position2 = 0
    current_post_position3 = 0

    yesterday_post_position1 = 0
    yesterday_post_position2 = 0
    yesterday_post_position3 = 0

    context = {
        'current_prompt_text': current_prompt_text,
        'yesterdays_prompt_text': yesterdays_prompt_text,
        'todays_entries': todays_entries,
    }

    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

@ensure_csrf_cookie
def explore(request):
    # Get all entries from today that have a location attached
    entries = JournalEntry.objects.filter(latitude__isnull=False, longitude__isnull=False, date=now().date())
    
    # Pass the entries to the template to load on map
    return render(request, 'explore.html', {'entries': entries})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def save_entry(request):
    if request.method == "POST":
        entry_text= request.POST.get("entry_text")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        
        if not latitude or not longitude:
            return HttpResponse("Location not provided", status=400)
        
        if entry_text: 
            JournalEntry.objects.create(userID=request.user, date=now().date(), entry=entry_text, latitude=latitude, longitude=longitude)
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

    today = todays_date()
 
    # this returns the prompt to the profile
    prompt_text = get_prompt(today)

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


@login_required
def toggle_like(request, entry_id):
    if request.method == 'POST':
        # Get the JournalEntry object by ID
        entry = get_object_or_404(JournalEntry, id=entry_id)

        # Toggle the like status
        if request.user in entry.liked_by.all():
            entry.liked_by.remove(request.user)  # Unlike the entry
        else:
            entry.liked_by.add(request.user)     # Like the entry
            
        # Save change to the database
        entry.save()

        # Return a JSON response with the updated like status and like count
        return JsonResponse({
            'is_liked': request.user in entry.liked_by.all(),
            'likes': entry.liked_by.count()  # Send the updated like count
        })

    return JsonResponse(status=400)

def todays_date():
    date = now().date()
    return date

def yesterdays_date():
    date = now().date() - timedelta(days=1)
    return date

def get_prompt(date):
    #this returns the prompt of the passed date
    prompt_text = "no prompt available..."  # default if there is no prompt
    try:
        prompt = Prompt.objects.get(date=date) #get the prompt for the day
        prompt_text = prompt.prompt  
    except Prompt.DoesNotExist:
        pass
    return prompt_text