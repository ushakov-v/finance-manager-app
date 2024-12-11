# Используем официальный Python образ
FROM python:3.9

# Установка зависимостей
RUN pip install --upgrade pip

# Копируем requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копируем исходный код
COPY . /app
WORKDIR /app

# Устанавливаем переменные окружения для Django
ENV DJANGO_ENV=production
ENV PYTHONUNBUFFERED 1

# Открываем порт для приложения
EXPOSE 8000

# Выполнение миграций и запуск сервера через gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn finance_manager_app.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
