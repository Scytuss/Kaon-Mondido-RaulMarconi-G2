
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role',
        'contact_number'
    )

    list_filter = ('role',)

    search_fields = (
        'user__username',
        'user__email'
    )
