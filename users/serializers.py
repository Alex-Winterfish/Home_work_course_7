from rest_framework import serializers

from ed_platform.serializers import LessonSerializer, CourseSerializer
from users.models import PaymentModel, CustomUser


class PaymentSerializer(serializers.ModelSerializer):
    lessons_info = LessonSerializer(read_only=True, source="paid_lesson")
    courses_info = CourseSerializer(read_only=True, source="paid_course")

    class Meta:
        model = PaymentModel
        fields = [
            "id",
            "payment_date",
            "cost",
            "payment_type",
            "student",
            "lessons_info",
            "courses_info",
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    user_payments = PaymentSerializer(many=True, read_only=True, source="student")

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password", "country", "phone", "user_payments"]
