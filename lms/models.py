from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса", help_text="Введите название курса")
    preview = models.ImageField(upload_to="lms/preview", blank=True, null=True, verbose_name="Превью (картинка)", help_text="Загрузите превью (картинка)",)
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True, help_text="Введите описание курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока", help_text="Введите название урока")
    preview = models.ImageField(upload_to="lms/preview", blank=True, null=True, verbose_name="Превью (картинка)", help_text="Загрузите превью (картинка)",)
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True, help_text="Введите описание урока")
    video = models.URLField(blank=True, null=True, verbose_name="Видео", help_text="Загрузите видео")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

