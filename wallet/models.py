from django.db import models
import uuid


class Wallet(models.Model):
    """
    Wallet model
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        )
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
        )
    
    def __str__(self):
        return f'{self.id}: {self.balance}'
    

class Operation(models.Model):
    """
    Operation model
    """

    class Status(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Deposit'
        WITHDRAW = 'WITHDRAW', 'Withdraw'

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='operations'
        )
    operation_type = models.CharField(
        max_length=8,
        choices=Status.choices
        )
    amount = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
        )
    
    def __str__(self):
        return f'{self.operation_type}: {self.amount}'