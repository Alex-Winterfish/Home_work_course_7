# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ed_platform.models import CourseModel, LessonModel
from users.models import PaymentModel, CustomUser
from users.permissions import IsModerPermission
from users.serializers import PaymentSerializer, CustomUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.services import (
    stripe_create_price,
    stripe_create_session,
    stripe_create_product,
)


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение пользователя :model:users.PaymentModel.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание экземпляра :model:users.PaymentModel.",
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка экземпляров :model:users.PaymentModel.",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Изменение экземпляра :model:users.PaymentModel.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное изменение экземпляра :model:users.PaymentModel.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление экземпляра :model:users.PaymentModel.",
    ),
)
class PaymentViewSet(ModelViewSet):
    """Контроллер для операций над :model:users.PaymentModel."""

    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = (
        "paid_course__name",
        "paid_lesson__name",
        "paid_lesson__description",
        "paid_course__description",
        "payment_type",
    )
    ordering_fields = ("payment_date",)

    def perform_create(self, serializer):

        payment = serializer.save(student=self.request.user)
        course = payment.paid_course
        lesson = payment.paid_lesson

        if course:  # условие для создания продукта курса в страйп
            course_name = CourseModel.objects.get(id=course.id).name
            course_description = CourseModel.objects.get(id=course.id).description
            stripe_create_product(name=course_name, description=course_description)
        if lesson:  # условие для создания продукта урока в страйп
            lesson_name = LessonModel.objects.get(id=lesson.id).name
            lesson_description = CourseModel.objects.get(id=lesson.id).description
            stripe_create_product(name=lesson_name, description=lesson_description)

        price = stripe_create_price(payment.cost)  # создаем цену
        session_id, payment_link = stripe_create_session(price)  # создаем сессию
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.payment_type = "Перевод"
        payment.save()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = [IsAuthenticated, ~IsModerPermission]
        elif self.action in ["retrieve", "update", "list"]:
            self.permission_classes = [IsModerPermission, IsAuthenticated]
        return super().get_permissions()


@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Получение пользователя :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Создание экземпляра :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Получение списка экземпляров :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Изменение экземпляра :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Частичное изменение экземпляра :model:users.CustomUser.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Удаление экземпляра :model:users.CustomUser.",
    ),
)
class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class MyTokenObtainPairView(TokenObtainPairView):
    """Аутентификация пользователя"""

    permission_classes = (AllowAny,)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token
