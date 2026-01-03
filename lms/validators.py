from django.core.exceptions import ValidationError
from urllib.parse import urlparse
import re


def validate_youtube_only(value):
    """
    Валидатор для проверки, что ссылка ведет только на youtube.com
    """
    if not value:
        return

    # Парсим URL
    parsed_url = urlparse(value)

    # Извлекаем доменное имя
    domain = parsed_url.netloc

    # Удаляем www. если есть
    if domain.startswith('www.'):
        domain = domain[4:]

    # Разрешенные домены YouTube
    allowed_domains = ['youtube.com', 'youtu.be']

    # Проверяем, что домен соответствует разрешенным
    is_allowed = any(allowed in domain for allowed in allowed_domains)

    if not is_allowed:
        raise ValidationError(
            'Разрешены только ссылки на YouTube (youtube.com, youtu.be)'
        )