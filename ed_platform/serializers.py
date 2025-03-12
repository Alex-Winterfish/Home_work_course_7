from rest_framework.serializers import ModelSerializer

from ed_platform.models import CourseModel


class CourseSerializer(ModelSerializer):
    class Meta:
        model = CourseModel
        fields = '__all__'