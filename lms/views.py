from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionDetailSerializer
from users.permissions import IsModer, IsModerAndUser


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Список курсов с уроками"
))
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerAndUser]
    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()



class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer]
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerAndUser]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerAndUser]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionAPIView(APIView):
    """
    API для управления подпиской пользователя на курс
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # Получаем course_id разными способами
        course_id = request.data.get('course_id') or kwargs.get('course_id')

        # Валидация
        if not course_id:
            return Response(
                {
                    "error": "Не указан course_id",
                    "example_request": {
                        "course_id": 1
                    },
                    "received_data": request.data
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course_id = int(course_id)
        except (ValueError, TypeError):
            return Response(
                {"error": "course_id должен быть числом"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем курс
        course_item = get_object_or_404(Course, id=course_id)

        # Ищем существующую подписку
        subscription = Subscription.objects.filter(
            owner=user,
            course=course_item
        ).first()

        if subscription:
            # Если подписка есть - удаляем
            subscription.delete()
            message = 'Подписка удалена'
            action = 'unsubscribed'
            is_subscribed = False
        else:
            # Если подписки нет - создаем
            Subscription.objects.create(owner=user, course=course_item)
            message = 'Подписка добавлена'
            action = 'subscribed'
            is_subscribed = True

        return Response({
            "message": message,
            "action": action,
            "is_subscribed": is_subscribed,
            "course": {
                "id": course_item.id,
                "name": course_item.name,
                "description": course_item.description
            },
            "user": {
                "id": user.id,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)


class SubscriptionListAPIView(APIView):
    """Получение списка подписок пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscriptions = Subscription.objects.filter(
            owner=request.user,
            is_active=True
        ).select_related('course')

        serializer = SubscriptionDetailSerializer(subscriptions, many=True)
        return Response(serializer.data)