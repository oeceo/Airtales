from django.contrib import admin
from airtalesapp.models import User, JournalEntry, Profile, Prompt, Reported

admin.site.register(User)
admin.site.register(JournalEntry)
admin.site.register(Profile)
admin.site.register(Prompt)
admin.site.register(Reported)