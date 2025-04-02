from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_customer', 'is_business', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('is_customer', 'is_business', 'file', 'location', 'tel', 'description', 'working_hours')
        }),
    )


