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


def index(request):
    date = selected_date(0)
    prompt_text = get_current_prompt() # Today's prompt
    return render(request, 'index.html', {'date': date, 'prompt_text': prompt_text})

def about(request):
    return render(request, 'about.html')

def topposts(request):
    return render(request, 'topposts.html')

@ensure_csrf_cookie
def explore(request):
    prompt_text = get_current_prompt()
    # Get all entries from today that have a location attached
    entries = JournalEntry.objects.filter(latitude__isnull=False, longitude__isnull=False, date=now().date())
    # Pass the entries to the template to load on map
    return render(request, 'explore.html', {'entries': entries, 'prompt_text': prompt_text})

def login(request):
    return render(request, 'login.html')

def terms(request):
    return render(request, 'terms.html')

def signup(request):
    return render(request, 'signup.html')

@login_required
def profile(request):

    today = selected_date(0)
    prompt_text = get_prompt(today) # Returns the prompt
    prior_entry = JournalEntry.objects.filter(userID=request.user, date=today).exists() # Checks if entry already made today
    previous_entries = JournalEntry.objects.filter(userID=request.user).exclude(date=today).order_by('-date') # Gets previous entries
    context = {
        'prompt_text': prompt_text,
        'prior_entry':prior_entry,  
        'journal_entries':previous_entries
    }
    return render(request, 'profile.html', context)

def save_entry(request):
    if request.method == "POST":
        entry_text = request.POST.get("entry_text")
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

def view_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id)
    return render(request, 'view_entry.html', entry)

def userjournal(request):
    return render(request, 'userjournal.html')

@login_required
def toggle_like(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(JournalEntry, id=entry_id) # Get the JournalEntry object by ID
        if request.user in entry.liked_by.all(): # Toggle the like status
            entry.liked_by.remove(request.user) # Unlike the entry
        else:
            entry.liked_by.add(request.user) # Like the entry
        entry.save() # Save change to the database
        return JsonResponse({ # Return a JSON response with the updated like status and like count
            'is_liked': request.user in entry.liked_by.all(),
            'likes': entry.liked_by.count()  # Send the updated like count
        })
    return JsonResponse(status=400)

def selected_date(no_of_days): # Number of days to go back
    return now().date() - timedelta(days=no_of_days)

def get_prompt(set_date): # Returns prompt based on date param
    prompt_text = "no prompt yet..."  # Default if no prompt found
    try:
        prompt = Prompt.objects.get(date=set_date)
        prompt_text = prompt.prompt  
    except Prompt.DoesNotExist:
        pass
    return prompt_text

def get_current_prompt():
    prompt_text = get_prompt(now().date())
    return prompt_text

def get_top_entry(set_date): # Returns entry with most likes based on date param
    top_entry = (JournalEntry.objects.filter(date=set_date)
                 .annotate(like_count=Count('liked_by'))
                 .order_by('-like_count')
                 .first() # Returns null if no entries found
    )
    if top_entry:
        return {
            "entry_text": top_entry.entry_text,
            "entry_likes": top_entry.like_count,
            "total_entries": get_total_entries(set_date),
        }
    else:
        return {"message": "No entries available yet"}

def get_total_entries(set_date):
    return JournalEntry.objects.filter(date=set_date).count()
    
def top_entry(request):
    try:
        offset_str = request.GET.get('offset', '0') # Get the offset number as a string
        offset = int(offset_str) if offset_str.isdigit() else 0 # Cast as an int for use in the methods

        set_date = selected_date(offset)
        entry_data = get_top_entry(set_date)

        if not isinstance(entry_data, dict):
            return JsonResponse({"error": f"Unexpected return type {type(entry_data)} from get_top_entry_data"}, status=500)

        return JsonResponse({
            "prompt_text": get_prompt(set_date),
            "entry_text": entry_data.get("entry_text", "No entries available"),
            "entry_likes": entry_data.get("entry_likes", 0),
            "total_entries": entry_data.get("total_entries", 0),
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)