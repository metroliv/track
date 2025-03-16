from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.track_period, name='track_period'),
     path('history/', views.cycle_history, name='cycle_history'),
     path('Feedback/', views.Feedback, name='Feedback'),
]
