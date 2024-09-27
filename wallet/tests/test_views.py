from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from wallet.models import Wallet, Operation
from wallet.serializers import WalletSerializer, OperationSerializer

from wallet.urls import router


class WalletViewSetTest(APITestCase):
    """
    Wallet viewset tests
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create some data for testing
        """

        cls.wallet = Wallet.objects.create(
            balance=100
            )

    

    def test_get_existing_wallet_detail_(self):
        """
        Test for accessing existing wallet details
        """

        response = self.client.get(reverse('wallet:wallet-detail', args=(self.wallet.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_non_existing_wallet_detail_(self):
        """
        Test for accessing non-existing wallet details
        """

        non_existing_wallet_id = str(self.wallet.id)[:-1] + ['a', 'b'][str(self.wallet.id)[-1] == 'a']

        response = self.client.get(reverse('wallet:wallet-detail', args=(non_existing_wallet_id,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OperationViewSetTest(APITestCase):
    """
    Operation viewset tests
    """

    @classmethod
    def setUpTestData(cls):
        """
        Create some data for testing
        """

        cls.wallet = Wallet.objects.create(
            balance=100
            )


    def test_create_operation_with_existing_wallet(self):
        """
        Test for creating operation with existing wallet
        """

        data = {
            'operation_type': 'DEPOSIT',
            'amount': 50
        }

        response = self.client.post(reverse('wallet:operation-list', args=(self.wallet.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_operation_with_non_existing_wallet(self):
        """
        Test for creating operation with existing wallet
        """

        data = {
            'operation_type': 'DEPOSIT',
            'amount': 50
        }

        non_existing_wallet_id = str(self.wallet.id)[:-1] + ['a', 'b'][str(self.wallet.id)[-1] == 'a']

        response = self.client.post(reverse('wallet:operation-list', args=(non_existing_wallet_id,)), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_withdraw_operation_with_enough_balance_wallet(self):
        """
        Test for creating withdraw operation with enough balance wallet
        """

        data = {
            'operation_type': 'WITHDRAW',
            'amount': 50
        }

        response = self.client.post(reverse('wallet:operation-list', args=(self.wallet.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_withdraw_operation_with_not_enough_balance_wallet(self):
        """
        Test for creating withdraw operation with not enough balance wallet
        """

        data = {
            'operation_type': 'WITHDRAW',
            'amount': 150
        }

        response = self.client.post(reverse('wallet:operation-list', args=(self.wallet.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_operation_without_amount(self):
        """
        Test for creating operation without amount
        """

        data = {
            'operation_type': 'WITHDRAW',
        }

        response = self.client.post(reverse('wallet:operation-list', args=(self.wallet.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_operation_without_operation_type(self):
        """
        Test for creating operation without amount
        """

        data = {
            'amount': 100,
        }

        response = self.client.post(reverse('wallet:operation-list', args=(self.wallet.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
