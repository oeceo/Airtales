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
from airtalesapp.forms import UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

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


@login_required
def profile(request):
    today = selected_date(0)

 
    # this returns the prompt to the profile
    prompt_text = get_prompt(today)

    #this checks if the user has already made a journal entry
    prior_entry = JournalEntry.objects.filter(userID=request.user, date=today).exists()
    todays_entry = JournalEntry.objects.filter(userID=request.user, date=today)
    today_toshow = todays_entry.entry if todays_entry else "No entry yet."
    #gets the previous journal entries
    previous_entries = list(JournalEntry.objects.filter(userID=request.user).exclude(date=today).order_by('-date')[:3])
    # prompt_text_1 = get_prompt(yesterday)
    previous_entry_1, previous_entry_2, previous_entry_3 = "No previous entry.", "No previous entry.", "No previous entry."
    prompt_text_1, prompt_text_2, prompt_text_3 = "No prompt available.", "No prompt available.", "No prompt available."
    previous_1, previous_2, previous_3 = None, None, None

    # prompt_text_1 = get_prompt(previous_entries[0].date)
    # prompt_text_2 = get_prompt(previous_entries[1].date)
    # prompt_text_3 = get_prompt(previous_entries[2].date)
    # previous_entry_1 = previous_entries[0].entry
    # previous_entry_2 = previous_entries[1].entry
    # previous_entry_3 = previous_entries[2].entry
    # previous_1 = previous_entries[0].date
    # previous_2 = previous_entries[1].date
    # previous_3 = previous_entries[2].date

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
        # 'prompt_text_0': prompt_text_0,
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
        'todays_entry': today_toshow

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

def top_liked_entry(date):
    
    top_entry = (JournalEntry.objects.filter(date=date) # Filter by date based on date param
                 .annotate(like_count=Count('liked_by')) # Counts likes
                 .order_by('-like_count')
                 .first() # Returns null if no entries found
    )

    return top_entry.entry if top_entry else "no entries available yet"




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


