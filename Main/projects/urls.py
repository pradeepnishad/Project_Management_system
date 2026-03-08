from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/assign/', views.assign_project_view, name='assign_project'),
    path('<int:pk>/status/', views.update_project_status, name='update_project_status'),
    path(
    "manager/assign/<int:pk>/",
    views.manager_assign_associates,
    name="manager_assign_associates"
),
    
]