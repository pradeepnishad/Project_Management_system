from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ManagerProfile, AssociateProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


admin.site.register(ManagerProfile)
admin.site.register(AssociateProfile)