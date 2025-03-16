from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta



class PeriodTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_period_date = models.DateField()
    cycle_length = models.IntegerField()
    next_period_date = models.DateField(blank=True, null=True)
    ovulation_date = models.DateField(blank=True, null=True)
    days_until_next = models.IntegerField(blank=True, null=True)  # New field

    def save(self, *args, **kwargs):
        """Automatically calculate next period date, ovulation date, and days remaining."""
        if self.last_period_date and self.cycle_length:
            self.next_period_date = self.last_period_date + timedelta(days=self.cycle_length)
            self.ovulation_date = self.last_period_date + timedelta(days=14)

            # Calculate days remaining
            today = date.today()
            self.days_until_next = max(0, (self.next_period_date - today).days)

        super().save(*args, **kwargs)  # Save the model

    def __str__(self):
        return f"{self.user.username} - {self.last_period_date}"



class PeriodCycle(models.Model):
    """Model to store previous period cycle history for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_period_date = models.DateField()
    cycle_length = models.IntegerField()
    next_period_date = models.DateField()
    ovulation_date = models.DateField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.last_period_date}"

    class Meta:
        verbose_name = "Period Cycle"
        verbose_name_plural = "Period Cycles"




class Feedback(models.Model):
    """Model for storing user feedback."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=1)  # Default user ID = 1
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.submitted_at}"


