from rest_framework.routers import SimpleRouter
from ed_platform.apps import EdPlatformConfig
from django.urls import path
from ed_platform.views import (
    CourseViewSet,
    LessonCreateAPI,
    LessonUpdateAPI,
    LessonRetrieveAPI,
    LessonListAPI,
    LessonDestroyAPI,
)

app_name = EdPlatformConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet)

urlpatterns = [
    path("lessons_list/", LessonListAPI.as_view(), name="lessons_list"),
    path("lesson_update/<int:pk>/", LessonUpdateAPI.as_view(), name="lesson_update"),
    path("lesson_create/", LessonCreateAPI.as_view(), name="lesson_create"),
    path(
        "lesson_retrieve/<int:pk>/", LessonRetrieveAPI.as_view(), name="lesson_retrieve"
    ),
    path("lesson_destroy/<int:pk>/", LessonDestroyAPI.as_view(), name="lesson_destroy"),
] + router.urls
