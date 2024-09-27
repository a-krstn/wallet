from django.core.management.base import BaseCommand

from wallet.models import Wallet, Operation


class Command(BaseCommand):
    """
    Class to fill the database (1 wallet, 2 operations)
    """

    def handle(self, *args, **options):
        # Deleting all existing wallets and operations from database
        Wallet.objects.all().delete()
        Operation.objects.all().delete()

        # Creating wallet
        wallet = Wallet.objects.create(balance=0)

