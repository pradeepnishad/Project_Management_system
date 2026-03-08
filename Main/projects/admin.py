from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'manager', 'status', 'priority_score')
    list_filter = ('status',)
    search_fields = ('title',)