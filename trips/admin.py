from django.contrib import admin
from .models import Trip, LogEntry

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'pickup_location', 'dropoff_location', 'current_location', 'cycle_hours_used', 'created_at')
    search_fields = ('pickup_location', 'dropoff_location', 'current_location')

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'date', 'driving_hours', 'on_duty_hours', 'off_duty_hours', 'sleeper_berth_hours', 'total_hours', 'remaining_hours', 'legal_warning')
    search_fields = ('trip__pickup_location', 'trip__dropoff_location', 'date')
