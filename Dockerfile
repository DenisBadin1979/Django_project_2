# Этап 1: Сборщик
FROM python:3.13-slim AS builder

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы с зависимостями
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей (включая dev-зависимости для сборки)
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-interaction --no-ansi --no-root

# Копируем весь проект
COPY . .

# Этап 2: Финальный образ
FROM python:3.13-slim

WORKDIR /app

# Установка системных зависимостей (только необходимые)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение из builder
COPY --from=builder /app/.venv .venv

# Копируем код приложения
COPY --from=builder /app /app

# Активируем виртуальное окружение
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000