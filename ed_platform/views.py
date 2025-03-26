# -*- coding: UTF-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ed_platform.models import CourseModel, LessonModel
from ed_platform.serializers import CourseSerializer, LessonSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwnerPermission, IsModerPermission


class CourseViewSet(ModelViewSet):
    '''ViewSet для операций над :model:ed_platform.CurseModel'''
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = (~IsModerPermission & IsAuthenticated,)
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = (IsOwnerPermission,)
        elif self.action == 'retrieve':
            self.permission_classes = (IsOwnerPermission | IsModerPermission,)

        return super().get_permissions()


class LessonListAPI(ListAPIView):
    '''Отображает список эклемпляров :model: ed_platform.LessonModel'''
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwnerPermission | IsModerPermission,)


class LessonRetrieveAPI(RetrieveAPIView):
    '''Отображает эклемпляр :model: ed_platform.LessonModel'''
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwnerPermission | IsModerPermission,)


class LessonCreateAPI(CreateAPIView):
    '''Создает экземпляр :model: ed_platform.LessonModel'''
    serializer_class = LessonSerializer
    permission_classes = (~IsModerPermission & IsAuthenticated,)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class LessonUpdateAPI(UpdateAPIView):
    '''Вносит изменения в эклемпляро :model: ed_platform.LessonModel'''
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwnerPermission,)

class LessonDestroyAPI(DestroyAPIView):
    '''Удаляет экземпляр :model: ed_platform.LessonModel'''
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwnerPermission,)

class SubscriptionAPIView(APIView):
    '''Контроллер для управления подиской :model: ed_platform.SubscriptionModel'''

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data
        print(course_id)

