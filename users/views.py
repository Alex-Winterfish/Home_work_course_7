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
from users.services import stripe_create_price, stripe_create_session


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

    def perform_create(self, serializer):

        payment = serializer.save(student=self.request.user)
        price = stripe_create_price(payment.cost)
        session_id, payment_link = stripe_create_session(price)
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
