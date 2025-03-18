from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from users.models import PaymentModel, CustomUser
from users.serializers import PaymentSerializer, CustomUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class PaymentViewSet(ModelViewSet):
    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ('paid_course__name', 'paid_lesson__name', 'paid_lesson__description',
                     'paid_course__description', 'payment_type')
    ordering_fields = ('payment_date',)

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token