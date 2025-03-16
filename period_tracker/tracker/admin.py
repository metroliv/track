from django.contrib import admin
from .models import PeriodTracker, Feedback

class PeriodTrackerAdmin(admin.ModelAdmin):
    """Admin settings for the PeriodTracker model."""
    
    list_display = ('user', 'last_period_date', 'cycle_length', 'next_period_date', 'ovulation_date', 'days_until_next')
    search_fields = ('user__username',)
    list_filter = ('last_period_date',)
    ordering = ('-last_period_date',)  # Orders records by most recent last period date

class FeedbackAdmin(admin.ModelAdmin):
    """Admin settings for the Feedback model."""
    
    list_display = ('user', 'submitted_at', 'message')
    search_fields = ('user__username', 'message')
    list_filter = ('submitted_at',)
    ordering = ('-submitted_at',)  # Orders by most recent feedback first

# Register models in Django Admin
admin.site.register(PeriodTracker, PeriodTrackerAdmin)
admin.site.register(Feedback, FeedbackAdmin)
