from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from transactions.models import Transaction
from authentication.models import User





#------------------------------------------------------------------------------
class Inventory(models.Model):
    amount = models.DecimalField(max_digits=60, decimal_places=5)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Total inventory: ' + str(self.amount)







#------------------------------------------------------------------------------
class InputHistory(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=30, decimal_places=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) +"|"+ str(self.created_at)















#------------------------------------------------------------------------------
class FeeRates(models.Model):
    withdrawal = models.DecimalField(max_digits=30, decimal_places=5)
    deposit = models.DecimalField(max_digits=30, decimal_places=5)
    transfer = models.DecimalField(max_digits=30, decimal_places=5)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)


    def __str__(self):
        return 'deposit_fee: '+str(self.deposit) +'|'+ 'withdrawal_fee: '+str(self.withdrawal) +'|'+ 'transfer_fee: '+str(self.transfer)






#------------------------------------------------------------------------------
class UserFeeRates(models.Model):
    users = models.ManyToManyField(User)
    fee = models.DecimalField(max_digits=30, decimal_places=5)

    def __str__(self):
        return str(self.users) +"|"+ str(self.fee)















#End
