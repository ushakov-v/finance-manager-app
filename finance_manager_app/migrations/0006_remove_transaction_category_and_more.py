# Generated by Django 4.2.16 on 2024-11-26 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_manager_app', '0005_remove_transaction_category_expense_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='category',
        ),
        migrations.AddField(
            model_name='transaction',
            name='category_expense',
            field=models.CharField(blank=True, choices=[('mandatory', 'Обязательные расходы'), ('food', 'Продукты'), ('car', 'Автомобиль'), ('entertainment', 'Развлечения'), ('household', 'Товары для дома'), ('selfcare', 'Забота о себе'), ('education', 'Образование'), ('miscellaneous', 'Разное')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='category_income',
            field=models.CharField(blank=True, choices=[('salary', 'Зарплата'), ('other', 'Другие источники')], max_length=50, null=True),
        ),
    ]
