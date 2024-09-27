from rest_framework import serializers

from .models import Wallet, Operation
from . import services


class WalletSerializer(serializers.ModelSerializer):
    """
    Wallet serializer
    """

    # operations = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'balance')


class OperationSerializer(serializers.ModelSerializer):
    """
    Operation serializer
    """

    wallet = serializers.ReadOnlyField(source='wallet.id')

    class Meta:
        model = Operation
        fields = ('wallet', 'operation_type', 'amount')   
