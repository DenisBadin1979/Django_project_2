from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone

@shared_task(name='send_update_course')
def send_update_course(user_email):
    subject = 'Ваш курс обновлен'
    message = 'Спасибо, что подписаны на наш курс. проверьте его обновили!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    return send_mail(subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,)

@shared_task
def block_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    inactive_users.update(is_active=False)


