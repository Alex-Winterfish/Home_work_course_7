# -*- coding: UTF-8 -*-
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ed_platform.models import CourseModel, LessonModel
from ed_platform.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = ['id', 'name', 'description', 'video_url']
        validators = [UrlValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons_info = LessonSerializer(many=True, read_only=True, source='lessons')

    def get_lessons_count(self, instance):
        return LessonModel.objects.filter(course=instance).count()

    class Meta:
        model = CourseModel
        fields = ['id', 'name', 'preview', 'description', 'lessons_count', 'lessons_info', 'owner']


