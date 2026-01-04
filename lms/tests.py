from http.client import responses
from unittest import TestCase

from rest_framework import response, status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from lms.models import Course, Lesson, Subscription
from users.models import User


class LmsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@test.pro")
        self.course = Course.objects.create(name="Экономика", description="Все про экономику")
        self.lesson = Lesson.objects.create(name="Введение в экономику", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Введение в экономику")

    def test_lesson_create(self):
        url = reverse("lms:lesson_create")
        data = {"name" : "Информатика"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_lesson_update(self):
        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        data = {"name" : "Макроэкономика"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Макроэкономика")


    def test_lesson_destroy(self):
        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        # data = response.json()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(),0)


class SimpleSubscriptionTest(APITestCase):
    """Упрощенные тесты подписки"""

    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com'
        )
        self.course = Course.objects.create(
            name='Test Course',
            owner=self.user
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.subscription_url = reverse('lms:subscription-toggle')

    def test_subscription_create_and_delete(self):
        """Основной тест: создание и удаление подписки"""
        # 1. Создаем подписку
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.id},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'subscribed')
        self.assertTrue(Subscription.objects.filter(
            owner=self.user,
            course=self.course
        ).exists())

        # 2. Удаляем подписку
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.id},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'unsubscribed')
        self.assertFalse(Subscription.objects.filter(
            owner=self.user,
            course=self.course
        ).exists())

