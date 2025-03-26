# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from ed_platform.models import CourseModel, LessonModel


class Command(BaseCommand):
    help = "Add courses and lessons in database"

    def handle(self, *args, **kwargs):
        CourseModel.objects.all().delete()
        LessonModel.objects.all().delete()

        courses = [
            {
                "name": "Математический анализ",
                "description": "Основы математического анализа"
            },
            {
                "name": "Начертательная геометрия",
                "description": "Основы начертательной геометрии"
            },
            {
                "name": "Органическая химия",
                "description": "Основы органической химии"
            }
        ]

        for course_data in courses:
            course, created = CourseModel.objects.get_or_create(**course_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Добавлен курс {course.name}id: {course.id}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Курс уже существует {course.name}, id: {course.id}'
                    )
                )

        lessons = [
            {
                "name": "Урок 1.",
                "description": "Введение в математический анализ",
                "preview": "",
                "course": CourseModel.objects.get(name='Математический анализ')
            },
            {
                "name": "Урок 2.",
                "description": "Основы математического анализа",
                "preview": "",
                "course": CourseModel.objects.get(name='Математический анализ')
            },
            {
                "name": "Урок 1.",
                "description": "Эпюра плоскости",
                "preview": "",
                "course": CourseModel.objects.get(name='Начертательная геометрия')
            },
            {
                "name": "Урок 2.",
                "description": "Пересечение плоскостей",
                "preview": "",
                "course": CourseModel.objects.get(name='Начертательная геометрия')
            },
            {
                "name": "Урок 3.",
                "description": "Проекции фигуры на плоскость",
                "preview": "",
                "course": CourseModel.objects.get(name='Начертательная геометрия')
            },
            {
                "name": "Урок 4.",
                "description": "Пересечение фигур",
                "preview": "",
                "course": CourseModel.objects.get(name='Начертательная геометрия')
            },
            {
                "name": "Урок 1.",
                "description": "Основы органики",
                "preview": "",
                "course": CourseModel.objects.get(name='Органическая химия')
            },
            {
                "name": "Урок 2.",
                "description": "Кристалическая решетка",
                "preview": "",
                "course": CourseModel.objects.get(name='Органическая химия')
            },
            {
                "name": "Урок 3.",
                "description": "Простейшие органические соединеия",
                "preview": "",
                "course": CourseModel.objects.get(name='Органическая химия')
            },
            {
                "name": "Урок 4.",
                "description": "Бензольыне кольца",
                "preview": "",
                "course": CourseModel.objects.get(name='Органическая химия')
            },
            {
                "name": "Урок 5.",
                "description": "Реакции органических соединеий",
                "preview": "",
                "course": CourseModel.objects.get(name='Органическая химия')
            },
            {
                "name": "Урок 6.",
                "description": "Сложные органические соединеия ",
                "preview": "",
                "course": CourseModel.objects.get(name='Органическая химия')
            }
        ]

        for lesson_data in lessons:
            lesson, created = LessonModel.objects.get_or_create(**lesson_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Добавлен урок {lesson.description} id: {lesson.id}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Урок уже существует {lesson.description} id: {lesson.id}'
                    )
                )