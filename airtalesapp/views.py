from django.shortcuts import render, redirect
from .models import JournalEntry
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
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
    return render(request, 'profile.html')

def userjournal(request):
    return render(request, 'userjournal.html')

def save_entry(request):
    if request.method == "POST":
        entry_text= request.POST.get("entry_text")
        if entry_text: 
            JournalEntry.objects.create(entry_text=entry_text)
            return redirect("success_page")
    return render(request, "form.html")

def profile(request):
    today = now().date()  # Get today's date
    prompt_text = "No prompt available for today."  # Default if no prompt exists
    try:
        prompt = Prompt.objects.get(date=today)
        prompt_text = prompt.prompt  # Get the actual prompt text
    except Prompt.DoesNotExist:
        pass  # Keep the default text if no prompt is found

    context = {
        'prompt_text': prompt_text,  # Pass the prompt to the template
    }

    return render(request, "profile.html", context)
