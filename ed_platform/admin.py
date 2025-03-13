from django.contrib import admin

from ed_platform.models import CourseModel, LessonModel


@admin.register(CourseModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "id")
    list_filter = ["name"]
    search_help_text = ("name",)

@admin.register(LessonModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "course", "id")
    list_filter = ["name"]
    search_help_text = ("name",)