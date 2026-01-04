from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="lms/preview",
        blank=True,
        null=True,
        verbose_name="Превью (картинка)",
        help_text="Загрузите превью (картинка)",
    )
    description = models.TextField(
        verbose_name="Описание курса",
        blank=True,
        null=True,
        help_text="Введите описание курса",
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите Владелена",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    preview = models.ImageField(
        upload_to="lms/preview",
        blank=True,
        null=True,
        verbose_name="Превью (картинка)",
        help_text="Загрузите превью (картинка)",
    )
    description = models.TextField(
        verbose_name="Описание урока",
        blank=True,
        null=True,
        help_text="Введите описание урока",
    )
    video = models.URLField(
        blank=True, null=True, verbose_name="Видео", help_text="Загрузите видео"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс",
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите Владелена",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription (models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Владелец",
        help_text="Укажите Владелена",
        related_name='subscriptions',
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name='subscriptions',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['owner', 'course']

    def __str__(self):
        return f"{self.owner.email} подписан на {self.course.name}"