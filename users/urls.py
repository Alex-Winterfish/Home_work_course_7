from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from users.apps import UsersConfig
from rest_framework.routers import SimpleRouter

from users.views import PaymentViewSet, MyTokenObtainPairView, CustomUserRegisterView, CustomUserViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register('payments', PaymentViewSet)
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny)), name='token_refresh'),
    path('users/register/', CustomUserRegisterView.as_view(), name='register')
              ] + router.urls