from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from finance_manager_app.models import Transaction  # Импортируем модель Transaction из приложения finance_manager_app


class TransactionModelTestCase(TestCase):
    """Тестовый класс для проверки модели Transaction"""

    def setUp(self):
        """Создание пользователя для тестов и транзакции"""
        # Создание пользователя, который будет использоваться в тестах
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создание и сохранение транзакции для тестирования
        self.transaction = Transaction(
            user=self.user,
            transaction_type='income',  # Тип транзакции: доход
            amount=100.50,  # Сумма транзакции
            date=date(2024, 12, 1),  # Дата транзакции
            description='Test income transaction',  # Описание транзакции
            category_income='salary'  # Категория дохода
        )
        self.transaction.save()  # Сохраняем транзакцию в базе данных

    def test_transaction_creation(self):
        """Проверка правильности создания транзакции"""
        transaction = self.transaction  # Получаем транзакцию для проверки
        self.assertEqual(transaction.transaction_type, 'income')  # Проверяем тип транзакции
        self.assertEqual(transaction.amount, 100.50)  # Проверяем сумму
        self.assertEqual(transaction.date, date(2024, 12, 1))  # Проверяем дату
        self.assertEqual(transaction.description, 'Test income transaction')  # Проверяем описание
        self.assertEqual(transaction.category_income, 'salary')  # Проверяем категорию дохода
        self.assertIsNone(transaction.category_expense)  # Для доходов категория расходов должна быть None

    def test_str_method(self):
        """Проверка работы метода __str__"""
        transaction = self.transaction  # Получаем транзакцию
        expected_str = 'Income - 100.5 - 2024-12-01'  # Ожидаемое строковое представление
        self.assertEqual(str(transaction), expected_str)  # Сравниваем с фактическим

    def test_category_expense_for_income(self):
        """Проверка, что для доходов категория расхода не может быть задана"""
        self.transaction.category_expense = 'food'  # Присваиваем категорию расхода
        with self.assertRaises(ValidationError):  # Проверяем, что ошибка валидации будет поднята
            self.transaction.save()  # Попытка сохранения должна вызвать ValidationError

    def test_category_income_for_expense(self):
        """Проверка, что для расходов категория дохода не может быть задана"""
        self.transaction.transaction_type = 'expense'  # Меняем тип транзакции на расход
        self.transaction.category_income = 'salary'  # Присваиваем категорию дохода, что неверно для расходов

        # Проверяем, что сохранение транзакции с категорией дохода для расхода вызывает ValidationError
        with self.assertRaises(ValidationError):  # Ожидаем, что будет вызвана ошибка валидации
            self.transaction.save()  # Попытка сохранения должна вызвать ValidationError

    def test_transaction_amount_validation(self):
        """Проверка, что сумма транзакции положительная"""
        # Попытка создать транзакцию с отрицательной суммой
        invalid_transaction = Transaction(
            user=self.user,
            transaction_type='expense',
            amount=-50.00,  # Невалидная сумма, должна вызывать ошибку
            date=date(2024, 12, 2),
            description='Invalid expense',
        )
        with self.assertRaises(ValueError):  # Ожидаем ValueError при попытке сохранить
            invalid_transaction.save()

    def test_transaction_description_length(self):
        """Проверка длины описания"""
        long_description = 'a' * 256  # Описание длиной 256 символов, что превышает максимально допустимую длину (255 символов)
        transaction = Transaction(
            user=self.user,
            transaction_type='income',
            amount=200.00,
            date=date(2024, 12, 1),
            description=long_description,  # Должно вызвать ошибку при сохранении
        )

        # Проверяем, что попытка сохранить транзакцию с длинным описанием вызывает ошибку
        with self.assertRaises(ValueError):  # Ожидаем ValueError при попытке сохранить
            transaction.save()


