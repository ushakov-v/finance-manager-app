from django.test import TestCase, Client
from django.urls import reverse
from app.models import Transaction  # Импортируем Transaction из app.models

class TransactionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.transaction = Transaction.objects.create(
            name="Grocery",
            amount=50,
            type="Expense"
        )

    def test_transaction_list_view(self):
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/transaction_list.html')

    def test_transaction_detail_view(self):
        response = self.client.get(reverse('transaction_detail', args=[self.transaction.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/transaction_detail.html')
