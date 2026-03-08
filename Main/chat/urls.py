from django.urls import path
from . import views

urlpatterns = [
    path('message/<int:pk>/edit/', views.edit_message, name='edit_message'),
    path('message/<int:pk>/delete/', views.delete_message, name='delete_message'),
]