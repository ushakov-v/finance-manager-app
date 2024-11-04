# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='transaction_list'),  # Список транзакций
    path('transactions/<int:id>/', views.transaction_detail, name='transaction_detail'),  # Детали транзакции
]
