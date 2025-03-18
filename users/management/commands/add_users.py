# -*- coding: UTF-8 -*-
import datetime

from django.core.management.base import BaseCommand
from users.models import CustomUser, PaymentModel
from ed_platform.models import CourseModel, LessonModel


class Command(BaseCommand):
    help = "Add users and payments"

    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()
        PaymentModel.objects.all().delete()

        users = [
            {
                "email": "example_1@mail.com",
                "country": "Russia",
                "username": "student_1",
                "password": "12345"
            },
            {
                "email": "example_2@mail.com",
                "country": "Russia",
                "username": "student_2",
                "password": "12345"
            }
        ]

        for user_data in users:
            user, created = CustomUser.objects.get_or_create(**user_data)
            if created:
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Добавлен пользователь {user.username}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Пользователь уже существует {user.username}'
                        )
                    )

        payments = [
            {
                "student": CustomUser.objects.get(username='student_1'),
                "paid_course": CourseModel.objects.get(name='Математический анализ'),
                "payment_date": datetime.date(2025,3,12),
                "cost": 10450,
                "payment_type": 'Наличные'
            },
            {
                "student": CustomUser.objects.get(username='student_1'),
                "paid_lesson": LessonModel.objects.get(description='Основы органики'),
                "payment_date": datetime.date(2025,3,13),
                "cost": 1345,
                "payment_type": 'Перевод'
            },
            {
                "student": CustomUser.objects.get(username='student_2'),
                "paid_course": CourseModel.objects.get(name='Начертательная геометрия'),
                "payment_date": datetime.date(2025,3,17),
                "cost": 12340,
                "payment_type": 'Перевод'
            },
            {
                "student": CustomUser.objects.get(username='student_2'),
                "paid_course": CourseModel.objects.get(name='Органическая химия'),
                "payment_date": datetime.date(2025,3,15),
                "cost": 15030,
                "payment_type": 'Наличные'
            },
            {
                "student": CustomUser.objects.get(username='student_2'),
                "paid_lesson": LessonModel.objects.get(description='Основы математического анализа'),
                "payment_date": datetime.date(2025,2,14),
                "cost": 1345,
                "payment_type": 'Перевод'
            }
        ]

        for payment_data in payments:
            payment, created = PaymentModel.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Студент {payment.student} внес оплату: {payment.payment_type}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Студент {payment.student} уже вносил оплату: {payment.payment_type}'
                    )
                )