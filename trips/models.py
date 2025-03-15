from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    current_latitude = models.FloatField(default=0.0)  
    current_longitude = models.FloatField(default=0.0)  
    dropoff_latitude = models.FloatField(default=0.0) 
    dropoff_longitude = models.FloatField(default=0.0)  
    cycle_hours_used = models.FloatField(default=0.0)  
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)  
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f"Trip {self.id}: {self.pickup_location} to {self.dropoff_location} ({'Active' if self.is_active else 'Completed'})"

class LogEntry(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField(auto_now_add=True)
    driving_hours = models.FloatField(default=0.0)
    on_duty_hours = models.FloatField(default=0.0)
    off_duty_hours = models.FloatField(default=0.0)
    sleeper_berth_hours = models.FloatField(default=0.0)
    total_hours = models.FloatField(default=0.0) 
    remaining_hours = models.FloatField(default=70.0) 
    legal_warning = models.CharField(max_length=500, blank=True, null=True)  

    class Meta:
        unique_together = ('trip', 'date') 

    def __str__(self):
        return f"Log for Trip {self.trip.id} on {self.date} (Remaining: {self.remaining_hours}h)"

@receiver(post_save, sender=Trip)
def create_log_entries(sender, instance, created, **kwargs):
    if created:
        total_hours = instance.cycle_hours_used
        remaining_hours = 70  
        max_daily_hours = 11 

        for day in range(int(total_hours // max_daily_hours) + 1):
            driving_hours = min(max_daily_hours, total_hours - (day * max_daily_hours))
            on_duty_hours = min(14, driving_hours + 3)  
            off_duty_hours = 24 - on_duty_hours 
            total_day_hours = driving_hours + on_duty_hours

            remaining_hours = max(0, remaining_hours - total_day_hours)

            legal_warning = None
            if remaining_hours <= 0:
                legal_warning = "⚠️"
            elif on_duty_hours > 14:
                legal_warning = "⚠️"
            elif driving_hours > 11:
                legal_warning = "⚠️"

            LogEntry.objects.create(
                trip=instance,
                driving_hours=driving_hours,
                off_duty_hours=off_duty_hours,
                sleeper_berth_hours=0,  
                on_duty_hours=on_duty_hours,
                total_hours=total_day_hours,
                remaining_hours=remaining_hours,
                legal_warning=legal_warning
            )
