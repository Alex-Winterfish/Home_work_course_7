from django.contrib import admin

from ed_platform.models import CourseModel, LessonModel


@admin.register(CourseModel)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "id")
    list_filter = ["name"]
    search_help_text = ("name",)


@admin.register(LessonModel)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "course", "id")
    list_filter = ["name"]
    search_help_text = ("name",)
