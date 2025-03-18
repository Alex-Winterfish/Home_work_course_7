from django.urls import path
from users.apps import UsersConfig
from rest_framework.routers import SimpleRouter

from users.views import PaymentViewSet, CustomUserViewSet, MyTokenObtainPairView

app_name = UsersConfig.name

router = SimpleRouter()
router.register('payments', PaymentViewSet)
router.register('users', CustomUserViewSet)

urlpatterns = [path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair')] + router.urls