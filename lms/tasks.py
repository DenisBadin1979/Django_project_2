from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


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



