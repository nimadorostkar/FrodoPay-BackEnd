from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.myusermanager import UserManager
from django.utils.html import format_html






#------------------------------------------------------------------------------
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    shop = models.CharField(max_length=254, null=True, blank=True)
    birthday = models.DateField(max_length=254, null=True, blank=True)
    photo = models.ImageField(upload_to='user/photo',default='user/photo/default.png', null=True, blank=True)
    referral = models.CharField(max_length=254, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    backend = 'authentication.mybackend.ModelBackend'

    def img(self):
        return format_html("<img width=30 src='{}'>".format(self.photo.url))

    def __str__(self):
        return str(self.email)











#End
