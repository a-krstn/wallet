from rest_framework import status
from rest_framework.response import Response

from .models import Wallet

from decimal import Decimal


def check_wallet(wallet_id, operation_type, amount):
    """
    Add info
    """

    wallet = Wallet.objects.get(id=wallet_id)
    if not wallet:
        return Response(
            {"error": "Wallet not found"},
            status=status.HTTP_404_NOT_FOUND
            )
    if operation_type == 'WITHDRAW' and wallet.balance < Decimal(amount):
        return Response(
            {"error": "There are not enough money on the wallet to make an operation"},
            status=status.HTTP_400_BAD_REQUEST
            )
    
    return wallet
    
    
