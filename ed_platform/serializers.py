from rest_framework.serializers import ModelSerializer

from ed_platform.models import CourseModel, LessonModel


class CourseSerializer(ModelSerializer):
    class Meta:
        model = CourseModel
        fields = '__all__'

class LessonSerializer(ModelSerializer):
    class Meta:
        model = LessonModel
        fields = '__all__'