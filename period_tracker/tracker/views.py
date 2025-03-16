from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import timedelta

from .forms import PeriodTrackerForm, FeedbackForm
from .models import PeriodTracker, Feedback
from datetime import timedelta, date



def register(request):
    """User Registration View"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registering
            return redirect('track_period')  # Ensure this matches urls.py
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def track_period(request):
    """Handles tracking period and saving it to the database"""
    period_data = None

    if request.method == 'POST':
        form = PeriodTrackerForm(request.POST)
        if form.is_valid():
            period_tracker = form.save(commit=False)
            period_tracker.user = request.user
            period_tracker.next_period_date = period_tracker.last_period_date + timedelta(days=period_tracker.cycle_length)
            period_tracker.ovulation_date = period_tracker.last_period_date + timedelta(days=14)
            period_tracker.save()

            # Calculate days remaining until the next period
            today = date.today()
            days_until_next = (period_tracker.next_period_date - today).days

            period_data = {
                'next_period_date': period_tracker.next_period_date,
                'ovulation_date': period_tracker.ovulation_date,
                'days_until_next': max(0, days_until_next)  # Ensure it doesn’t show negative days
            }
    else:
        form = PeriodTrackerForm()

    return render(request, 'track_period.html', {'form': form, 'period_data': period_data})


@login_required
def user_logout(request):
    """Logs out the user"""
    logout(request)
    return redirect('login')  # Ensure this matches urls.py


@login_required
def cycle_history(request):
    """Displays period tracking history"""
    history = PeriodTracker.objects.filter(user=request.user).order_by('-last_period_date')
    return render(request, 'tracker/cycle_history.html', {'history': history})


@login_required
def Feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Assign the logged-in user
            feedback.save()
            return redirect('feedback_success')  # Redirect to a success page
    else:
        form = FeedbackForm()
    
    return render(request, 'tracker/feedback.html', {'form': form})



@login_required
def feedback_success(request):
    """Displays a success message after feedback submission"""
    return HttpResponse("Thank you for your feedback!")

