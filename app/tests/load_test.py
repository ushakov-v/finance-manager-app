from locust import HttpUser, task, between
from random import randint
from time import sleep
import re


class FinanceManagerUser(HttpUser):
    wait_time = between(1, 50)  # Время ожидания между задачами пользователя

    def on_start(self):
        """Получаем CSRF токен и логинимся перед выполнением задач."""
        # Выполняем GET-запрос для получения CSRF токена
        response = self.client.get("/register/")
        csrf_token = self.extract_csrf_token(response.text)  # Извлекаем CSRF токен из HTML
        self.csrf_token = csrf_token  # Сохраняем CSRF токен

        # Выполняем регистрацию и логин (если необходимо)
        self.register_and_login()

    def extract_csrf_token(self, html):
        """Извлекаем CSRF токен из HTML."""
        # Ищем CSRF токен в HTML-коде с помощью регулярного выражения
        match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', html)
        return match.group(1) if match else None  # Возвращаем токен, если найден

    def get_headers(self):
        """Возвращаем заголовки с CSRF токеном для POST-запросов."""
        return {
            "X-CSRFToken": self.csrf_token,  # Заголовок с CSRF токеном
            "Content-Type": "application/x-www-form-urlencoded"  # Указываем тип контента
        }

    def register_and_login(self):
        """Регистрируем и логинимся."""
        # Генерация уникального имени для регистрации
        username = f"user{randint(1, 1000)}"  # случайное имя пользователя
        password = "password123"  # фиксированный пароль
        email = f"{username}@example.com"  # создание уникального адреса электронной почты

        # Регистрация пользователя
        registration_data = {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,
            'csrfmiddlewaretoken': self.csrf_token  # добавляем CSRF токен для безопасности
        }
        self.client.post('/register/', registration_data, headers=self.get_headers())  # Выполняем POST-запрос для регистрации

        # Обновляем CSRF токен после регистрации
        response = self.client.get('/accounts/login/')
        self.csrf_token = self.extract_csrf_token(response.text)  # Извлекаем новый CSRF токен

        # Логин пользователя
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': self.csrf_token  # добавляем CSRF токен
        }
        self.client.post('/accounts/login/', login_data, headers=self.get_headers())  # Выполняем POST-запрос для логина

        # Обновляем CSRF токен после логина
        self.csrf_token = self.extract_csrf_token(response.text)  # Извлекаем новый CSRF токен

    @task(1)
    def view_transactions(self):
        """Тестирование получения списка транзакций."""
        self.client.get('/transactions')  # Выполняем GET-запрос для получения списка транзакций
        sleep(2)  # Ждем 2 секунды между запросами

    @task(2)
    def add_transaction(self):
        """Тестирование добавления новой транзакции."""
        # Создаем данные для новой транзакции с случайной суммой
        data = {
            'transaction_type': 'income',  # Тип транзакции
            'amount': randint(10, 1000),  # Случайная сумма
            'date': '2024-12-01',  # Фиксированная дата для простоты
            'description': 'Test Transaction'  # Описание транзакции
        }
        self.client.post('/add/', data, headers=self.get_headers())  # Выполняем POST-запрос для добавления транзакции
        sleep(2)  # Ждем 2 секунды

    @task(3)
    def edit_transaction(self):
        """Тестирование редактирования транзакции."""
        transaction_id = randint(1, 100)  # Генерируем случайный ID транзакции для редактирования
        # Данные для редактирования транзакции
        data = {
            'transaction_type': 'expense',  # Новый тип транзакции
            'amount': randint(10, 1000),  # Случайная сумма
            'date': '2024-12-01',  # Фиксированная дата
            'description': 'Edited Test Transaction'  # Новое описание
        }
        self.client.post(f'/edit/{transaction_id}/', data, headers=self.get_headers())  # Выполняем POST-запрос для редактирования
        sleep(2)  # Ждем 2 секунды

    @task(4)
    def delete_transaction(self):
        """Тестирование удаления транзакции."""
        transaction_id = randint(1, 100)  # Генерируем случайный ID транзакции для удаления
        # Отправляем запрос на удаление, как если бы пользователь сразу нажал "Да" в попапе
        self.client.post(f'/delete/{transaction_id}/', headers=self.get_headers())  # Выполняем POST-запрос на удаление
        sleep(2)  # Ждем 2 секунды

    @task(5)
    def view_profile(self):
        """Тестирование доступа к профилю пользователя (требует логина)."""
        self.client.get('/profile/')  # Выполняем GET-запрос для получения профиля пользователя
        sleep(2)  # Ждем 2 секунды

    @task(6)
    def logout(self):
        """Тестирование выхода из системы."""
        self.client.get('/logout/', headers=self.get_headers())  # Выполняем GET-запрос для выхода из системы
        sleep(2)  # Ждем 2 секунды


# Повторные задачи (повторные запросы с задержкой)
class RepeatedUser(FinanceManagerUser):
    wait_time = between(5, 10)  # Более длинная задержка между повторными запросами
