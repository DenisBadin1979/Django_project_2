from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.views import LessonListAPIView
from users.apps import UsersConfig
from users.views import PaymentViewSet, PaymentListAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),

]
urlpatterns += router.urls