# -*- coding: UTF-8 -*-
from rest_framework import status
from rest_framework.test import APITestCase
from ed_platform.models import LessonModel, CourseModel
from users.models import CustomUser


class LessonsTestCase(APITestCase):
    """Тестирование для :model:ed_platform.LessonModel"""

    def setUp(self):
        user_data = {
            "username": "test_user_1",
            "email": "test_user_1@mail.com",
            "password": "12345",
        }

        self.test_user = CustomUser.objects.create_user(**user_data)

        self.lesson_1 = LessonModel.objects.create(
            name="Test_lesson_1",
            description="Description of lesson 1",
            owner=self.test_user,
        )
        self.lesson_2 = LessonModel.objects.create(
            name="Test_lesson_2",
            description="Description of lesson 2",
            owner=self.test_user,
        )
        self.client.force_authenticate(user=self.test_user)

    def test_get_lesson(self):
        """Тестирование получения курса"""

        request = self.client.get(f"/lesson_retrieve/{self.lesson_1.pk}/")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        print(request.json())

        self.assertEqual(
            request.json(),
            {
                "id": self.lesson_1.pk,
                "name": "Test_lesson_1",
                "description": "Description of lesson 1",
                "video_url": None,
            },
        )

    def test_get_lessons_list(self):
        """Тестироване получения списка уроков"""

        request = self.client.get("/lessons_list/")

        print(request.json())

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(
            request.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson_1.pk,
                        "name": "Test_lesson_1",
                        "description": "Description of lesson 1",
                        "video_url": None,
                    },
                    {
                        "id": self.lesson_2.pk,
                        "name": "Test_lesson_2",
                        "description": "Description of lesson 2",
                        "video_url": None,
                    },
                ],
            },
        )

    def test_lesson_create(self):
        """Тестирование создания экземпляра курса"""

        data = {
            "name": "Test_lesson_3",
            "description": "Description of lesson 3",
            "video_url": "http://www.youtube.com/exemple",
        }

        request = self.client.post("/lesson_create/", data=data)

        print(request.json())

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

        request = self.client.get(
            "/lessons_list/"
        )  # получаем список уроков для проверки добавления

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(
            request.json(),
            {
                "count": 3,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson_1.pk,
                        "name": "Test_lesson_1",
                        "description": "Description of lesson 1",
                        "video_url": None,
                    },
                    {
                        "id": self.lesson_2.pk,
                        "name": "Test_lesson_2",
                        "description": "Description of lesson 2",
                        "video_url": None,
                    },
                    {
                        "id": self.lesson_2.pk + 1,
                        "name": "Test_lesson_3",
                        "description": "Description of lesson 3",
                        "video_url": "http://www.youtube.com/exemple",
                    },
                ],
            },
        )

    def test_lesson_delete(self):
        """Тестирование удаления урока"""

        request = self.client.delete(f"/lesson_destroy/{self.lesson_1.pk}/")

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_update(self):
        """Тестирование обновление урока"""

        data = {
            "name": "Test_lesson_1",
            "description": "UPDATED Description of lesson 1",
            "video_url": "http://www.youtube.com/exemple",
        }

        request = self.client.patch(f"/lesson_update/{self.lesson_2.pk}/", data=data)

        print(request.json())

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        request = self.client.get(f"/lesson_retrieve/{self.lesson_2.pk}/")

        self.assertEqual(
            request.json(),
            {
                "id": self.lesson_2.pk,
                "name": "Test_lesson_1",
                "description": "UPDATED Description of lesson 1",
                "video_url": "http://www.youtube.com/exemple",
            },
        )


class SubscriptionTestCase(APITestCase):
    """Тестирование :model:ed_platform.SubscriptionModel"""

    def setUp(self):

        user_data = {
            "username": "test_user_1",
            "email": "test_user_1@mail.com",
            "password": "12345",
        }

        self.test_user = CustomUser.objects.create_user(**user_data)

        self.course = CourseModel.objects.create(
            name="Test_courese",
            description="Description of test course",
        )

    def test_subscribe(self):
        """Тестирование оформления и отмены подписки на курс"""
        self.client.force_authenticate(user=self.test_user)

        request = self.client.post(f"/subscribe/{self.course.pk}/")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(request.json(), {"message": "подписка оформлена"})

        request = self.client.post(f"/subscribe/{self.course.pk}/")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(request.json(), {"message": "подписка отменена"})
