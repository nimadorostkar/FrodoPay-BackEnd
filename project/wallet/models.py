from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from authentication.models import User
import uuid





#------------------------------------------------------------------------------
class Wallet(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  wallet_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
  inventory = models.DecimalField(max_digits=19, decimal_places=10)
  date_created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return str(self.id)
