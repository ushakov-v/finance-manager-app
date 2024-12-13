from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from finance_manager_app.models import Transaction
from datetime import datetime

class TransactionViewTests(TestCase):
    """Тесты для представлений транзакций (View)"""

    def setUp(self):
        """Создаем тестового пользователя и данные для тестов"""
        # Создаем пользователя для выполнения тестовых действий
        self.user = User.objects.create_user(username='testuser', password='password123')
        # Логинимся под созданным пользователем для выполнения последующих действий
        self.client.login(username='testuser', password='password123')

    def test_transaction_list_view(self):
        """Тестируем отображение списка транзакций"""
        # Создаем тестовую транзакцию
        transaction = Transaction.objects.create(
            transaction_type='income',  # Тип транзакции: доход
            amount=100.00,  # Сумма транзакции
            description='Test income',  # Описание транзакции
            user=self.user,  # Привязываем транзакцию к тестовому пользователю
            date=datetime.now()  # Указываем текущую дату
        )
        # Делаем GET-запрос на страницу списка транзакций
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)  # Проверяем, что статус код 200 (OK)
        self.assertContains(response, 'Test income')  # Проверяем, что транзакция отображается на странице

    def test_add_transaction_view(self):
        """Тестируем добавление транзакции"""
        # Данные для добавления новой транзакции
        data = {
            'amount': 100.00,  # Сумма
            'transaction_type': 'income',  # Тип транзакции
            'description': 'Test income',  # Описание
            'date': datetime.now().strftime('%Y-%m-%d')  # Указываем текущую дату в правильно формате
        }
        # Отправляем POST-запрос для добавления транзакции
        response = self.client.post(reverse('add_transaction'), data)
        # Проверяем, что произошло перенаправление на страницу со списком транзакций
        self.assertRedirects(response, reverse('transaction_list'))
        # Проверяем, что новая транзакция была успешно добавлена в базу данных
        self.assertTrue(Transaction.objects.filter(description='Test income').exists())

    def test_edit_transaction_view(self):
        """Тестируем редактирование транзакции"""
        # Создаем транзакцию для редактирования
        transaction = Transaction.objects.create(
            transaction_type='income',  # Тип транзакции: доход
            amount=100.00,  # Сумма
            description='Old income',  # Существующее описание
            user=self.user,  # Привязываем транзакцию к тестовому пользователю
            date=datetime.now()  # Указываем дату
        )
        # Данные для обновления транзакции
        data = {
            'amount': 150.00,  # Новая сумма
            'transaction_type': 'income',  # Тип транзакции
            'description': 'Updated income',  # Новое описание
            'date': datetime.now().strftime('%Y-%m-%d')  # Указываем дату
        }
        # Отправляем POST-запрос для редактирования транзакции
        response = self.client.post(reverse('edit_transaction', kwargs={'pk': transaction.pk}), data)
        # Проверяем, что произошло перенаправление на страницу со списком транзакций
        self.assertRedirects(response, reverse('transaction_list'))
        transaction.refresh_from_db()  # Обновляем объект транзакции из базы данных, чтобы получить изменения
        # Проверяем, что описание было обновлено
        self.assertEqual(transaction.description, 'Updated income')

    def test_delete_transaction_view(self):
        """Тестируем удаление транзакции"""
        # Создаем транзакцию для удаления
        transaction = Transaction.objects.create(
            transaction_type='income',  # Тип транзакции: доход
            amount=100.00,  # Сумма
            description='Test income',  # Описание транзакции
            user=self.user,  # Привязываем транзакцию к тестовому пользователю
            date=datetime.now()  # Указываем дату
        )
        # Отправляем POST-запрос для удаления транзакции
        response = self.client.post(reverse('delete_transaction', kwargs={'pk': transaction.pk}))
        # Проверяем, что произошло перенаправление на страницу со списком транзакций
        self.assertRedirects(response, reverse('transaction_list'))
        # Проверяем, что транзакция была успешно удалена из базы данных
        self.assertFalse(Transaction.objects.filter(pk=transaction.pk).exists())
