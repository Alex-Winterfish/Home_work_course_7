# -*- coding:utf-8 -*-
from rest_framework import permissions

from ed_platform.models import CourseModel, LessonModel
from users.serializers import CustomUserSerializer


class IsModerPermission(permissions.BasePermission):
    message = 'Доступ открыт только модераторам'

    def has_permission(self, request, view):
        return request.user.groups(name='moder').exists()

class IsStudentPermission(permissions.BasePermission):
    message = 'Доступ открыт только вледельцу'

    @staticmethod
    def payment_sort(payment):
        ''' Метод для накопления id курсов и id уроков в одном платеже.'''

        lessons_id = list()  # список для накопления id уроков
        courses_id = list()  # список для накопления id курсов
        courses = payment.get('courses_info')  # курсы пользователя
        lessons = payment.get('lessons_info')  # уроки пользователя
        if courses:
            if type(courses) is list:  # проверяем на наличие нескольких курсов
                for course in courses:
                    courses_id.append(course.get('id'))  # добавляем курс в итоговый список курсов
                    lessons_in_course = course.get('lessons_info')  # получаем уроки из курса
                    for lesson in lessons_in_course:
                        lessons_id.append(lesson.get('id'))  # добавляем уроки из курса в итоговый список уроков
            else:
                courses_id.append(courses.get('id'))  # добавляем курс в итоговый список курсов
                lessons_in_course = courses.get('lessons_info')

                for lesson in lessons_in_course:
                    lessons_id.append(lesson.get('id'))  # добавляем уроки из курса в итоговый список уроков

        elif lessons:
            if type(lessons) is list:  # проверяем на наличие нескольких уроков
                for lesson in lessons:
                    lessons_id.append(lesson.get('id'))
            else:
                lessons_id.append(lessons.get('id'))

        return courses_id, lessons_id


    def get_purchase_id(self, serialized_data):
        '''Метод для получения курсов и уроков, купленных пользователем.'''
        lessons_id = list()  # список для накопления id уроков
        courses_id = list()  # список для накопления id курсов
        user_payments = serialized_data.get('user_payments') #получаем курсы и уроки пользователя
        if type(user_payments) is list: #проверяем на наличие нескольких покупок
            for payment in user_payments:
                course, lesson = self.payment_sort(payment)
                courses_id.extend(course)
                lessons_id.extend(lesson)
        else:
            course, lesson = self.payment_sort(user_payments)
            courses_id.extend(course)
            lessons_id.extend(lesson)

        return courses_id, lessons_id


    def has_object_permission(self, request, view, obj):
        user = request.user
        serialized_data = CustomUserSerializer(user).data
        courses_id, lessons_id = self.get_purchase_id(serialized_data)
        if isinstance(obj, CourseModel):
            return obj.id in courses_id
        elif isinstance(obj, LessonModel):
            return obj.id in lessons_id


