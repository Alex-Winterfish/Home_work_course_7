# -*- coding: UTF-8 -*-
import datetime
import os

from django.core.mail import send_mail

from ed_platform.models import LessonModel, SubscriptionModel, CourseModel

from celery import shared_task
from django.utils import timezone

from users.models import CustomUser


@shared_task
def send_lesson_update(request, action):
    '''Сервисная функция для оповещения подписчика об изменении урока.'''
    lesson_id = request.parser_context.get("kwargs").get(
        "pk"
    )  # Получаем id урока из запроса
    lesson = LessonModel.objects.get(id=lesson_id)
    course = lesson.course
    subscription = SubscriptionModel.objects.filter(course=course)
    recipient_list = list()
    for sub in subscription:
        recipient_list.append(sub.user)
    if action == 'update':
        subject = "Обновился курс из ваших подписок!"
        message = f"В курсе \"{course.name}\" обновлен урок \"{lesson.name}\"!"
    if action == 'delete':
        subject = "Изменения в ваших подписках!"
        message = f"В курсе \"{course.name}\" удален урок \"{lesson.name}\"!"
    from_email = os.getenv("EMAIL_HOST_USER")
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_course_update(course_id):
    '''Оповещения подписчика об изменении курса.'''
    course = CourseModel.objects.get(id=course_id)
    subscription = SubscriptionModel.objects.filter(course=course)
    recipient_list = list()
    for sub in subscription:
        recipient_list.append(sub.user)
    subject = "Изменения в ваших подписках!"
    message = f"Изменен курс \"{course.name}\"!"
    from_email = os.getenv("EMAIL_HOST_USER")
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def user_deactivate():
    '''Блокировка пользователей по времени бездействия'''
    inactive = timezone.now() - datetime.timedelta(days=30)

    users = CustomUser.objects.filter(last_login__lt=inactive)

    for user in users:
        user.is_active = False

