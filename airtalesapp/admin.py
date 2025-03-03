from django.contrib import admin
from airtalesapp.models import User, JournalEntry, Profile, Prompt

# Register your models here.
admin.site.register(User)
admin.site.register(JournalEntry)
admin.site.register(Profile)
admin.site.register(Prompt)

