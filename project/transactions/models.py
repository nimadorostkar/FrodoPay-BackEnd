from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from wallet.models import Wallet





#------------------------------------------------------------------------------
class Transaction(models.Model):
    source = models.CharField(max_length=254, null=True, blank=True)
    destination = models.CharField(max_length=254, null=True, blank=True)
    amount = models.DecimalField(max_digits=30, decimal_places=5)
    CHOICES1 = (('deposit','deposit'),('transfer','transfer'),('withdrawal','withdrawal'))
    type = models.CharField(max_length=254, choices=CHOICES1)
    CHOICES2 = (('success','success'),('fail','fail'),('pending','pending'))
    status = models.CharField(max_length=254, choices=CHOICES2)
    description = models.CharField(max_length=254, null=True, blank=True)
    fee = models.DecimalField(max_digits=30, decimal_places=5, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type +"|"+ self.status +"|"+ self.source






'''
#------------------------------------------------------------------------------
class Fee(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='transaction')
    amount = models.DecimalField(max_digits=30, decimal_places=5)

    def __str__(self):
        return str(self.id) +"|"+ str(self.amount)

    class Meta:
        verbose_name = "Transaction fee"
        verbose_name_plural = "Transactions fee"

'''












#End
