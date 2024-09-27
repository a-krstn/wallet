from django.test import TestCase
from django.contrib.auth import get_user_model

from wallet.models import Wallet, Operation


class WalletModelTests(TestCase):
    """
    Wallet model tests
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create some data for testing
        """

        cls.wallet = Wallet.objects.create(
            balance=100
            )
        
    def test_str_method(self):
        """
        String wallet form testing
        """

        self.assertEqual(str(self.wallet), f'{self.wallet.id}: {self.wallet.balance}')


class OperationModelTests(TestCase):
    """
    Operation model tests
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create some data for testing
        """

        wallet = Wallet.objects.create(
            balance=100
            )

        cls.operation = Operation.objects.create(
            wallet=wallet,
            operation_type='DEPOSIT',
            amount=100
            )
        
    def test_str_method(self):
        """
        String Operation form testing
        """

        self.assertEqual(str(self.operation), f'{self.operation.operation_type}: {self.operation.amount}')
