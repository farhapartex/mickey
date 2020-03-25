from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "created_by")

@admin.register(Tag)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published", "archive", "created_by")
    search_fields = ['title','category__name','published']