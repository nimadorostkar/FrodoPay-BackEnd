from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from authentication.models import User
import uuid





#------------------------------------------------------------------------------
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    inventory = models.DecimalField(max_digits=30, decimal_places=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.wallet_id)
