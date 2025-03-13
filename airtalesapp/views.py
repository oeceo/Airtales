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
from django.db.models import Count
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login



def index(request):
    
    today = selected_date(0)
    yesterday = selected_date(1)
    day_before = selected_date(2)

    prompt_text_0 = get_prompt(today)
    prompt_text_1 = get_prompt(yesterday)
    prompt_text_2 = get_prompt(day_before)

    top_entry_0 = top_liked_entry(today)
    top_entry_1 = top_liked_entry(yesterday)
    top_entry_2 = top_liked_entry(day_before)

    context = {
        'prompt_text_0': prompt_text_0,
        'prompt_text_1': prompt_text_1,
        'prompt_text_2': prompt_text_2,
        'top_entry_0': top_entry_0,
        'top_entry_1': top_entry_1,
        'top_entry_2': top_entry_2,
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

    today = selected_date(0)
 
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

# login page
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print("User authenticated:", user)
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('airtalesapp:profile')  # Redirect to users homepage
        else:
            print("User NOT authenticated:", user)
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'login.html')




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

def selected_date(no_of_days): # Number of days to go back
    date = now().date() - timedelta(days=no_of_days)
    return date

def get_prompt(date):
    #this returns the prompt of the passed date
    prompt_text = "no prompt available..."  # default if there is no prompt
    try:
        prompt = Prompt.objects.get(date=date) # Gets the prompt for the day
        prompt_text = prompt.prompt  
    except Prompt.DoesNotExist:
        pass
    return prompt_text

def top_liked_entry(date):
    top_entry = (JournalEntry.objects.filter(date=date) # Filter by date based on date param
                .annotate(like_count=Count('liked_by')) # Counts likes
                .order_by('-like_count')
                .first() # Returns null if no entries found
    )

    return top_entry.entry if top_entry else "no entries available yet"


# JOURNAL ENTRY PAGE

@login_required
def journal_entries(request):
    # Get the current year and month from the request parameters or use default values
    year = request.GET.get('year', 2025)  # Default to 2025
    month = request.GET.get('month', 3)   # Default to March
    print(f"Retrieving journal entries for user {request.user} and {year} {month}")
    
    # Filter the journal entries by the given year and month
    entries = JournalEntry.objects.filter(date__year=year, date__month=month, userID=request.user)

    # Get available years and months
    available_years = JournalEntry.objects.filter(userID=request.user).values('date__year').distinct().order_by('date__year')
    available_months = range(1, 13)  # Months 1 to 12
    
    # Prepare the context
    context = {
        'journal_entries': entries,
        'available_years': [entry['date__year'] for entry in available_years],  # Extract years
        'available_months': available_months,
        'selected_year': year,
        'selected_month': month
    }
    
    return render(request, 'userjournal.html', context)