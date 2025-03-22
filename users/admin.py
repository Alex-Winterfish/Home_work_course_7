from django.contrib import admin
from users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone", "username")
    list_filter = ["email"]
    search_help_text = ("email",)

@admin.register(LessonModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "course", "id")
    list_filter = ["name"]
    search_help_text = ("name",)