from ed_platform.models import CourseModel, LessonModel
from ed_platform.serializers import CourseSerializer, LessonSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwnerPermission


class CourseViewSet(ModelViewSet):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer


class LessonListAPI(ListAPIView):
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer




class LessonRetrieveAPI(RetrieveAPIView):
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwnerPermission,)

class LessonCreateAPI(CreateAPIView):
    serializer_class = LessonSerializer

class LessonUpdateAPI(UpdateAPIView):
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer

class LessonDestroyAPI(DestroyAPIView):
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
