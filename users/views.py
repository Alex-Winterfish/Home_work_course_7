# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import PaymentModel, CustomUser
from users.permissions import IsModerPermission
from users.serializers import PaymentSerializer, CustomUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class PaymentViewSet(ModelViewSet):
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

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = ~IsModerPermission
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = (IsModerPermission, IsAuthenticated)


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        return Response("Для регистрации пользователя используйте url: users/register/")


class CustomUserRegisterView(CreateAPIView):
    """Представление для регистрации пользователя"""

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token
