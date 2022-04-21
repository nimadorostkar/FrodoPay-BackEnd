from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from authentication.models import User
from shortuuid.django_fields import ShortUUIDField



#------------------------------------------------------------------------------
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_id = ShortUUIDField(unique=True, length=22, max_length=40, primary_key=False, alphabet="abcdefg1234", editable=False)
    inventory = models.DecimalField(max_digits=30, decimal_places=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.wallet_id)