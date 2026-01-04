from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField, URLField
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_youtube_only


class LessonSerializer(ModelSerializer):
    video = URLField(
        validators=[validate_youtube_only],
        required=False,
        allow_blank=True
    )

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

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """
        Проверяем, подписан ли текущий пользователь на этот курс
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Проверяем наличие активной подписки
            return Subscription.objects.filter(
                owner=request.user,
                course=obj,
                is_active=True
            ).exists()
        return False


    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lessons", "count_lesson", "is_subscribed"]


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.name', read_only=True)
    user_email = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'course_id', 'course_title', 'user_email', 'created_at', 'is_active']



