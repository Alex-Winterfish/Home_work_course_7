from ed_platform.models import CourseModel, LessonModel
from ed_platform.serializers import CourseSerializer #LessonSerializer
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

class CourseViewSet(ModelViewSet):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer

