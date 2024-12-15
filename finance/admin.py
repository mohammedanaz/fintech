from django.contrib import admin
from .models import *

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'source', 'category', 'created_at', 'updated_at')
    search_fields = ('user', 'amount', 'category')

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)