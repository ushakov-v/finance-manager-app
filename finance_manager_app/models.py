from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    CATEGORY_INCOME = [
        ('salary', 'Зарплата'),
        ('other', 'Другие источники'),
    ]

    CATEGORY_EXPENSE = [
        ('mandatory', 'Обязательные расходы'),
        ('food', 'Продукты'),
        ('car', 'Автомобиль'),
        ('entertainment', 'Развлечения'),
        ('household', 'Товары для дома'),
        ('selfcare', 'Забота о себе'),
        ('education', 'Образование'),
        ('miscellaneous', 'Разное'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255)

    category_income = models.CharField(max_length=50, choices=CATEGORY_INCOME, null=True, blank=True)
    category_expense = models.CharField(max_length=50, choices=CATEGORY_EXPENSE, null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.amount} - {self.date}"
