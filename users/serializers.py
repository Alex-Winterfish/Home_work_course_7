# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ed_platform.models import SubscriptionModel
from ed_platform.serializers import LessonSerializer, CourseSerializer
from users.models import PaymentModel, CustomUser


class PaymentSerializer(serializers.ModelSerializer):
    lessons_info = LessonSerializer(read_only=True, source="paid_lesson")
    courses_info = CourseSerializer(read_only=True, source="paid_course")

    class Meta:
        model = PaymentModel
        fields = [
            "id",
            "paid_course",
            "paid_lesson",
            "payment_date",
            "cost",
            "payment_type",
            "student",
            "lessons_info",
            "courses_info",
            "session_id",
            "payment_link",
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    user_payments = PaymentSerializer(many=True, read_only=True, source="student")
    user_subscriptions = SerializerMethodField()

    def get_user_subscriptions(self, instance):
        """Метод для получения курсов, на которые подписан пользователь."""
        sub_list = list()
        user_subs = SubscriptionModel.objects.filter(
            user=instance
        )  # получаем подписки пользователя
        for sub in user_subs:
            sub_list.append(
                sub.course.id
            )  # создаем список курсов на которые подписан пользователь
        return sub_list

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "password",
            "country",
            "phone",
            "user_payments",
            "user_subscriptions",
        ]
