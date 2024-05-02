from django.contrib import admin
from django.contrib.admin import register
from .models import Product, Category

@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
