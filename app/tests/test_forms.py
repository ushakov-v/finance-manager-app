# from django.test import TestCase
# from .forms import TransactionForm
#
# class TransactionFormTest(TestCase):
#     def test_valid_data(self):
#         form = TransactionForm(data={
#             'name': "Utilities",
#             'amount': 100,
#             'type': "Expense"
#         })
#         self.assertTrue(form.is_valid())
#
#     def test_invalid_data(self):
#         form = TransactionForm(data={})
#         self.assertFalse(form.is_valid())
#         self.assertEqual(len(form.errors), 3)  # Проверяем наличие ошибок в 3 полях
