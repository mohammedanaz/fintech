from django.contrib import admin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'role', 'is_active', 'created_at', 'updated_at')
    search_fields = ('email', 'first_name', 'last_name')
