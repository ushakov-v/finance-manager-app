FROM python:3.9

# Установка зависимостей
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копирование исходного кода
COPY . /app
WORKDIR /app

# Установка переменных окружения
ENV DJANGO_ENV=production

# Выполнение миграций и запуск сервера
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]