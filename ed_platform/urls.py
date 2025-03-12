from rest_framework.routers import SimpleRouter
from ed_platform.apps import EdPlatformConfig
from ed_platform.views import CourseViewSet
app_name = EdPlatformConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [] + router.urls