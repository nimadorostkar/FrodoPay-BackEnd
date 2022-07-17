from django.db import models
from django.urls import reverse
from django.dispatch import receiver







#------------------------------------------------------------------------------
class Advertise(models.Model):
    image = models.ImageField(upload_to='advertise/image')
    link = models.CharField(max_length=256)

    def __str__(self):
        return str(self.image)
