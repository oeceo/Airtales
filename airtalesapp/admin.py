from django.contrib import admin
from airtalesapp.models import Reported, User, JournalEntry, Profile, Prompt

admin.site.register(User)

admin.site.register(Profile)
admin.site.register(Prompt)
admin.site.register(Reported)

# Custom admin class for filtering reported journal entries
class ReportedJournalEntryAdmin(admin.ModelAdmin):
    list_display = ('userID', 'date', 'entry', 'isReported')
    list_filter = ('isReported',)
    search_fields = ('userID__username', 'date', 'entry')
    actions = ['delete_selected_entries']

    def get_queryset(self, request):
        """Filter to show only reported entries"""
        queryset = super().get_queryset(request)
        return queryset.filter(isReported=True)

    def delete_selected_entries(self, request, queryset):
        """Custom action to delete selected reported entries"""
        queryset.delete()
    delete_selected_entries.short_description = "Delete selected reported entries"

# Register Reported Entries section separately
admin.site.register(JournalEntry, ReportedJournalEntryAdmin)