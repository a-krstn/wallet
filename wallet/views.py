from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from .models import Wallet, Operation
from .serializers import WalletSerializer, OperationSerializer
from . import services

from decimal import Decimal


class WalletAPIView(generics.RetrieveAPIView):
    """
    Wallet view
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'id'


class WalletViewSet(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin):
    """
    Wallet viewset
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'id'


class OperationViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin):
    """
    Operation view
    """

    queryset = Operation.objects.all()
    serializer_class = OperationSerializer

    def create(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(id=kwargs['wallet_id'])
        except ObjectDoesNotExist:
            return Response(
                {"error": "Wallet not found"},
                status=status.HTTP_404_NOT_FOUND
                )

        if 'operation_type' not in request.data:
            raise ValidationError(['Operation type field is required.'])

        if 'amount' not in request.data:
            raise ValidationError(['Amount field is required.'])
        
        operation_type = request.data['operation_type']
        amount = Decimal(request.data['amount'])

        if operation_type == 'WITHDRAW' and wallet.balance < amount:
            return Response(
                {"error": "There are not enough money on the wallet to make an operation"},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(wallet=wallet)

        wallet.balance += [amount, -amount][operation_type == 'WITHDRAW']
        wallet.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
