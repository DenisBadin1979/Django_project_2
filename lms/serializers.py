from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    # def get_lessons(self, course):
    #     return list(course.lesson_set.values_list('name','description', flat=True))

    count_lesson = SerializerMethodField()

    def get_count_lesson(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lessons", "count_lesson"]
