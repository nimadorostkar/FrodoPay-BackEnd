from django.db import models
from django.urls import reverse
from authentication.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField








#------------------------------------------------------------------------------
class Transaction(models.Model):
    source = models.CharField(max_length=256, null=True, blank=True)
    destination = models.CharField(max_length=256, null=True, blank=True)
    amount = models.DecimalField(max_digits=30, decimal_places=5)
    CHOICES1 = (('deposit','deposit'),('transfer','transfer'),('withdrawal','withdrawal'))
    type = models.CharField(max_length=256, choices=CHOICES1)
    CHOICES2 = (('success','success'),('fail','fail'),('pending','pending'))
    status = models.CharField(max_length=256, choices=CHOICES2)
    description = models.TextField(max_length=256, null=True, blank=True)
    fee = models.DecimalField(max_digits=30, decimal_places=5, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type +"|"+ self.status +"|"+ str(self.source)

    def normalize_amount(self):
        return str(self.amount.normalize())

    def normalize_fee(self):
        return str(self.fee.normalize())




















#------------------------------------------------------------------------------
class WithdrawalCeiling(models.Model):
    monthly = models.DecimalField(max_digits=30, decimal_places=5, default=0)
    daily = models.DecimalField(max_digits=30, decimal_places=5, default=0)


    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)


    def __str__(self):
        return 'monthly: '+str(self.monthly) +'|'+ 'daily: '+str(self.daily)












#------------------------------------------------------------------------------
class DepoHash(models.Model):
    TOKEN = (
        ('BUSD', 'BUSD'),
        ('BTC', 'BTC'),
        ('ETH', 'ETH'),
        ('USDT', 'USDT'),
    )
    NETWORK = (
        ('ERC20', 'ERC20'),
        ('BEP20', 'BEP20'),
    )
    amount = models.DecimalField(max_digits=30, decimal_places=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=60, choices=TOKEN)
    network = models.CharField(max_length=60, choices=NETWORK)
    deposit_id = ShortUUIDField(unique=True, length=16, max_length=40, alphabet="abcdefg1234", primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.deposit_id) +'|'+str(self.user.username)








#End
