from django.urls import path
from .views import client_signup

urlpatterns = [
    path('signup/', client_signup, name='signup'),
]