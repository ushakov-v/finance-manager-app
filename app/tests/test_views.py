from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from finance_manager_app.models import Transaction
from django.utils import timezone


class TransactionViewTestCase(TestCase):

    def setUp(self):
        """Создаем пользователя и транзакцию для тестов"""
        self.user = User.objects.create_user(username='testuser', password='password')  # Создание тестового пользователя
        self.transaction = Transaction.objects.create(
            transaction_type='income',  # Тип транзакции (доход)
            amount=100,  # Сумма транзакции
            date=timezone.now(),  # Дата транзакции
            description='Test transaction',  # Описание транзакции
            user=self.user  # Связываем транзакцию с созданным пользователем
        )
        self.client.login(username='testuser', password='password')  # Логинимся как тестовый пользователь

    def test_add_transaction_view(self):
        """Тестирование страницы добавления транзакции"""
        url = reverse('add_transaction')  # Получаем URL для страницы добавления транзакции
        response = self.client.get(url)  # Выполняем GET-запрос
        self.assertEqual(response.status_code, 200)  # Проверяем, что статус ответа 200 (успешно)
        self.assertTemplateUsed(response, 'add_transaction.html')  # Проверяем, что используется правильный шаблон
        self.assertContains(response, 'Добавить новую транзакцию')  # Проверяем наличие текста на странице

    def test_edit_transaction_view(self):
        """Тестирование страницы редактирования транзакции"""
        url = reverse('edit_transaction', kwargs={'pk': self.transaction.pk})  # URL для редактирования транзакции
        response = self.client.get(url)  # Выполняем GET-запрос
        self.assertEqual(response.status_code, 200)  # Проверка статуса ответа
        self.assertTemplateUsed(response, 'edit_transaction.html')  # Проверка шаблона
        self.assertContains(response, 'Редактировать транзакцию')  # Проверка текста на странице

    def test_delete_transaction_view(self):
        """Тестирование страницы удаления транзакции"""
        url = reverse('delete_transaction', kwargs={'pk': self.transaction.pk})  # URL для удаления транзакции
        response = self.client.get(url)  # Выполняем GET-запрос
        self.assertEqual(response.status_code, 200)  # Проверка статуса ответа
        self.assertTemplateUsed(response, 'delete_transaction.html')  # Проверка шаблона
        self.assertContains(response, 'Вы уверены, что хотите удалить эту транзакцию?')  # Проверка текста

    def test_transaction_list_view(self):
        """Тестирование страницы списка транзакций"""
        url = reverse('transaction_list')  # URL для списка транзакций
        response = self.client.get(url)  # Выполняем GET-запрос
        self.assertEqual(response.status_code, 200)  # Проверка статуса ответа
        self.assertTemplateUsed(response, 'transaction_list.html')  # Проверка шаблона
        self.assertContains(response, 'Мои транзакции')  # Проверка текста на странице списка
        self.assertContains(response, 'Test transaction')  # Проверка наличия тестовой транзакции

    def test_post_add_transaction(self):
        """Тестирование POST-запроса для добавления транзакции"""
        url = reverse('add_transaction')  # URL для добавления транзакции
        data = {
            'transaction_type': 'income',  # Тип транзакции
            'amount': 200,  # Сумма транзакции
            'date': '2024-12-01',  # Дата транзакции
            'description': 'New test transaction'  # Описание новой транзакции
        }
        response = self.client.post(url, data)  # Выполняем POST-запрос с данными
        self.assertEqual(response.status_code, 302)  # Проверка редиректа (302)
        self.assertTrue(Transaction.objects.filter(description='New test transaction').exists())  # Проверка создания транзакции

    def test_post_edit_transaction(self):
        """Тестирование POST-запроса для редактирования транзакции"""
        url = reverse('edit_transaction', kwargs={'pk': self.transaction.pk})  # URL для редактирования
        data = {
            'transaction_type': 'income',  # Новый тип транзакции
            'amount': 150,  # Новая сумма транзакции
            'date': '2024-12-01',  # Новая дата
            'description': 'Edited transaction'  # Новое описание
        }
        response = self.client.post(url, data)  # Выполняем POST-запрос
        self.assertEqual(response.status_code, 302)  # Проверка редиректа (302)
        self.transaction.refresh_from_db()  # Обновление экземпляра транзакции из базы данных
        self.assertEqual(self.transaction.amount, 150)  # Проверка изменения суммы
        self.assertEqual(self.transaction.description, 'Edited transaction')  # Проверка изменения описания

    def test_post_delete_transaction(self):
        """Тестирование POST-запроса для удаления транзакции"""
        url = reverse('delete_transaction', kwargs={'pk': self.transaction.pk})  # URL для удаления
        response = self.client.post(url)  # Выполняем POST-запрос
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после удаления
        self.assertFalse(Transaction.objects.filter(pk=self.transaction.pk).exists())  # Проверка, что транзакция удалена
