from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from wallet.models import Wallet




#------------------------------------------------------------------------------
class Transaction(models.Model):
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=30, decimal_places=5)
    CHOICES = ( ('increase','increase'), ('decrease','decrease'), ('withdrawal','withdrawal') )
    status = models.CharField(max_length=254, choices=CHOICES)
    description = models.CharField(max_length=254, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status +"|"+ str(self.wallet.wallet_id)
