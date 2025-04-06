# -*- coding: UTF-8 -*-
import datetime
import os

from django.core.mail import send_mail

from ed_platform.models import SubscriptionModel, CourseModel

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def send_course_update(course_id):
    """Оповещения подписчика об изменении курса."""
    course = CourseModel.objects.get(id=course_id)
    subscription = SubscriptionModel.objects.filter(course=course)
    recipient_list = list()
    for sub in subscription:
        recipient_list.append(sub.user)
    subject = "Изменения в ваших подписках!"
    message = f'Изменен курс "{course.name}"!'
    from_email = os.getenv("EMAIL_HOST_USER")
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def user_deactivate():
    """Блокировка пользователей по времени бездействия"""
    inactive = timezone.now() - datetime.timedelta(days=30)

    users = CustomUser.objects.filter(last_login__lt=inactive)

    for user in users:
        user.is_active = False
