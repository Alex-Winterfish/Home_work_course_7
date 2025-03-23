# -*- coding: UTF-8 -*-
import datetime

from django.core.management.base import BaseCommand
from users.models import CustomUser, PaymentModel
from ed_platform.models import CourseModel, LessonModel





class Command(BaseCommand):
    help = "Add users and payments"

    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()
        CourseModel.objects.all().delete()
        LessonModel.objects.all().delete()

        users = [
            {
                "email": "owner@mail.com",
                "username": "Owner",
                "password": "pbkdf2_sha256$870000$cXDyxcfpSsVnOEgcjD0hd9$e8pQZzj6Q5G5P9MYSjAhJ7He5FEOxhktOcasUGtOxAQ=",
                "country": "Russia",
            },
            {
                "email": "owner_1@mail.com",
                "username": "Owner_1",
                "password": "pbkdf2_sha256$870000$k9lZWga6YEePGlyyoZZp0u$dACFQOuJB1EzKRCTvNwnMkr105fVqJ2vUYzsSv9WldQ=",
                "country": "Russia",
            },
            {
                "email": "moderator@mail.com",
                "username": "Moderator",
                "password": "pbkdf2_sha256$870000$qZpBGpbQhswmuhaD5UeGMU$LJQBE2FgTxFfl3axz4cAYbSW9iratOKUxMVA9qsAX58=",
                "country": "Russia",
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

        courses = [
                {
                    "id": 33,
                    "name": "Русская литература",
                    "description": "Изучение русской литературы",
                    "owner": CustomUser.objects.get(email="owner@mail.com")
                },
                {
                    "id": 32,
                    "name": "Математический анализ",
                    "description": "Угдубленное зучение геометрии",
                    "owner": CustomUser.objects.get(email="owner@mail.com")
                },
                {
                    "id": 35,
                    "name": "Русский Ч+",
                    "description": "Угдубленное языка",
                    "owner": CustomUser.objects.get(email="owner_1@mail.com")
                }
            ]

        for courses_data in courses:
            course, created = CourseModel.objects.get_or_create(**courses_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Создан курс {course.name}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Курс {course.name} уже существует'
                    )
                )

        lessons = [
                    {
                        "id": 95,
                        "name": "Подлежащие и сказуеиое",
                        "description": "Углубленное языка",
                        "owner": CustomUser.objects.get(email="owner_1@mail.com")

                    },
                    {
                        "id": 96,
                        "name": "Синтаксис языка",
                        "description": "Углубленное языка",
                        "owner": CustomUser.objects.get(email="owner_1@mail.com")
                    },
                    {
                        "id": 98,
                        "name": "ЛОгарифмы",
                        "description": "Изучение логарифмов",
                        "owner": CustomUser.objects.get(email="owner@mail.com")

                    },
                    {
                        "id": 99,
                        "name": "ЛОгарифмы",
                        "description": "Изучение логарифмов",
                        "owner": CustomUser.objects.get(email="owner@mail.com")
                    },
                    {
                        "id": 100,
                        "name": "ЛОгарифмы",
                        "description": "Изучение логарифмов",
                        "owner": CustomUser.objects.get(email="owner@mail.com")
                    }
                ]

        for lessons_data in lessons:
            lesson, created = LessonModel.objects.get_or_create(**lessons_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Создан урок {lesson.name}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Урок {lesson.name} уже существует'
                    )
                )