from django.contrib import admin
from .models import Category, Task, User


class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "telegram_id"]
    search_fields = ["name", "telegram_id"]
    list_per_page = 10


class TaskAdmin(admin.ModelAdmin):
    list_display = ["category", "status", "title", "description", "created_at", "due_date", "user"]
    search_fields = ["title"]
    list_filter = ("category", "status", "user")
    list_per_page = 10


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]
    list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
