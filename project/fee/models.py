from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from transactions.models import Transaction






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
        return self.type +"|"+ self.status +"|"+ str(self.source)










#End
