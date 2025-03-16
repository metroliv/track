from django import forms
from django.contrib.auth.models import User
from .models import PeriodTracker, Feedback


class PeriodTrackerForm(forms.ModelForm):
    """Form for tracking period cycle details."""
    
    class Meta:
        model = PeriodTracker
        fields = ['last_period_date', 'cycle_length']
        widgets = {
            'last_period_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cycle_length': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'last_period_date': "Last Period Date",
            'cycle_length': "Cycle Length (days)",
        }


class RegisterForm(forms.ModelForm):
    """User registration form with password confirmation."""
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': "Username",
            'email': "Email Address",
        }

    def clean(self):
        """Validate password confirmation."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        """Save the user with a hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Securely hash the password
        if commit:
            user.save()
        return user


class FeedbackForm(forms.ModelForm):
    """Form for submitting user feedback."""
    
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your feedback...'}),
        }
        labels = {
            'message': "Your Feedback",
        }
