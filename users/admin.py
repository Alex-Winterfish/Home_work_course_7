from django.contrib import admin
from users.models import CustomUser, PaymentModel


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone", "username")
    list_filter = ["email"]
    search_help_text = ("email",)


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("student", "paid_course", "paid_lesson")
    list_filter = ["student"]
    search_help_text = ("student",)
