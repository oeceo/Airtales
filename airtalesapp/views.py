import json
from django.forms import BooleanField
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from .models import JournalEntry, Reported
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.utils.timezone import timedelta
from django.views.decorators.csrf import csrf_exempt
from .models import Prompt 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, ExpressionWrapper
from airtalesapp.forms import UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.core import serializers


User = get_user_model()

def index(request):
    date = selected_date(0)
    prompt_text = get_current_prompt()
    return render(request, 'index.html', {'date': date, 'prompt_text': prompt_text})

def about(request):
    return render(request, 'about.html')

def topposts(request):
    return render(request, 'topposts.html')

@ensure_csrf_cookie
def explore(request):
    # Get all entries from today that have a location attached
    prompt_text = get_current_prompt()
    
    context = {
        'prompt_text': prompt_text,
    }
    
    # Pass the entries to the template to load on map
    return render(request, 'explore.html', context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        User = get_user_model()        
        user = authenticate(username=email, password=password)
        # try:
        #     user = User.objects.get(email=email)
        # except User.DoesNotExist:
        #     return HttpResponse("Invalid login details.")
        if user is not None:
            # if user.is_active:
                login(request, user)
                return redirect('airtalesapp:profile')
            # else:
                # return HttpResponse("Invalid Login.")
        else:
            # print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    return render(request, 'login.html')
    # return render(request, 'login.html')

def terms(request):
    return render(request, 'terms.html')

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.userID = user 
            profile.save()
            registered = True
            return redirect('airtalesapp:login')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request,'signup.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'registered': registered
                })

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

@login_required
def profile(request):
    today = selected_date(0)
    prompt_text = get_prompt(today)

    #this checks if the user has already made a journal entry
    prior_entry = JournalEntry.objects.filter(userID=request.user, date=today).exists()
    if prior_entry: 
        todays_entry = JournalEntry.objects.get(userID=request.user, date=today).entry
    else:
        todays_entry = "No entry yet."
    #gets the previous journal entries
    previous_entries = list(JournalEntry.objects.filter(userID=request.user).exclude(date=today).order_by('-date')[:3])
    previous_entry_1, previous_entry_2, previous_entry_3 = "No previous entry.", "No previous entry.", "No previous entry."
    prompt_text_1, prompt_text_2, prompt_text_3 = "No prompt available.", "No prompt available.", "No prompt available."
    previous_1, previous_2, previous_3 = None, None, None

    if len(previous_entries) > 0:
        previous_entry_1 = previous_entries[0].entry
        prompt_text_1 = get_prompt(previous_entries[0].date)
        previous_1 = previous_entries[0].date
    if len(previous_entries) > 1:
        previous_entry_2 = previous_entries[1].entry
        prompt_text_2 = get_prompt(previous_entries[1].date)
        previous_2 = previous_entries[1].date
    if len(previous_entries) > 2:
        previous_entry_3 = previous_entries[2].entry
        prompt_text_3 = get_prompt(previous_entries[2].date)
        previous_3 = previous_entries[2].date

    context = {
        'prompt_text': prompt_text,
        'prior_entry':prior_entry,  
        'journal_entries':previous_entries,
        'prompt_text_1': prompt_text_1,
        'prompt_text_2': prompt_text_2,
        'prompt_text_3': prompt_text_3,
        'previous_entry_1' : previous_entry_1,
        'previous_entry_2' : previous_entry_2,
        'previous_entry_3' : previous_entry_3,
        'today':today,
        'yesterday':previous_1,
        'day_before':previous_2,
        'two_days_ago':previous_3,
        'todays_entry': todays_entry 

    }
    
    return render(request, 'profile.html', context)

def view_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id)
    return render(request, 'view_entry.html', entry)

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

def get_entry(date, userID):
    #this returns the prompt of the passed date
    # Filter by date based on date param
    entry_text = "entry does not exist"
    #prompt_text = "no prompt available..."  # default if there is no prompt
    try:
        entry = JournalEntry.objects.get(userID=userID,date=date)
        entry_text = entry.entry

        # prompt = Prompt.objects.get(date=date) # Gets the prompt for the day
        # prompt_text = prompt.prompt  
    except JournalEntry.DoesNotExist:
        pass
    return entry_text

@login_required  # Ensure the user is authenticated
def report_entry(request, entry_id):
    if request.method == 'POST':
        try:
            # Ensure entry exists and the user is not reporting their own entry
            entry = JournalEntry.objects.get(id=entry_id)
            if entry.userID == request.user:
                return JsonResponse({"message": "You cannot report your own entry."}, status=400)

            # Create the report and mark the entry as reported
            Reported.objects.create(userID=request.user, entryID=entry, date=entry.date)
            entry.isReported = True
            entry.save()
            return JsonResponse({"message": "Entry reported successfully."})

        except JournalEntry.DoesNotExist:
            return JsonResponse({"message": "Entry not found."}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=400)

@login_required
def all_entries(request):
    if request.method == "GET":
        # Get all entries from today that have a location attached
        entries = JournalEntry.objects.filter(latitude__isnull=False, longitude__isnull=False, date=now().date())
        
        context = {
            'entries': serializers.serialize('json', entries)
        }
        return JsonResponse(context)
    return JsonResponse({"message": "Invalid request method."}, status=400)

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

# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = ProfileForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = ProfileForm()

#     return render(request,
#                 'signup.html',
#                 context = {'user_form': user_form,
#                 'profile_form': profile_form,
#                 'registered': registered
#                 })

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect(reverse('airtalesapp:index'))
#             else:
#                 return HttpResponse("Your account is disabled.")
#         else:
#             print(f"Invalid login details: {username}, {password}")
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'airtalesapp/login.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect("airtalesapp:login")  # Redirect to login page

@login_required
def journal_entries(request):
    # Get the current year and month from the request parameters or use default values
    year = request.GET.get('year', 2025)  # Default to 2025
    month = request.GET.get('month', 3)   # Default to March
    
    print(f"Retrieving journal entries for user {request.user} and {year} {month}")
    
    # Filter the journal entries by the given year and month
    entries = JournalEntry.objects.filter(date__year=year, date__month=month, userID=request.user)

    # Create a list of prompts matching the entry dates
    prompts = Prompt.objects.filter(date__in=[entry.date for entry in entries])
    prompts_dict = {prompt.date: prompt.prompt for prompt in prompts}

    # Fetch the respective prompt for each entry
    for entry in entries:
        entry.prompt_text = prompts_dict.get(entry.date, "No prompt assigned")
    

    # Get available years and months
    available_years = JournalEntry.objects.filter(userID=request.user).values('date__year').distinct().order_by('date__year')
    available_months = range(1, 13)  # Months 1 to 12
    
    # Prepare the context
    context = {
        'journal_entries': entries,
        'available_years': [entry['date__year'] for entry in available_years], 
        'available_months': available_months,
        'selected_year': year,
        'selected_month': month
    }
    
    return render(request, 'userjournal.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, userID=request.user) 

    if request.method == "POST":
        entry.delete()
    
    return redirect('airtalesapp:userjournal')  
