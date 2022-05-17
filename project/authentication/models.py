from django.db import models
from django.contrib.auth.models import AbstractUser
#from authentication.myusermanager import UserManager
from django.utils.html import format_html






#------------------------------------------------------------------------------
class Countries(models.Model):
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=254, unique=True)
    flag = models.ImageField(upload_to='countries/flag', default='countries/flag/unknown.png')

    def flagImg(self):
        return format_html("<img width=30 src='{}'>".format(self.flag.url))

    def __str__(self):
        return str(self.name)








#------------------------------------------------------------------------------
class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    shop = models.CharField(max_length=254, null=True, blank=True)
    birthday = models.DateField(max_length=254, null=True, blank=True)
    country = models.ForeignKey(Countries, null=True, blank=True , on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user/photo',default='user/photo/default.png', null=True, blank=True)
    CHOICES = ( ('male','male'), ('female','female'), ('unspecified','unspecified') )
    gender = models.CharField(max_length=254, default='unspecified', choices=CHOICES, null=True, blank=True)
    referral = models.CharField(max_length=254, null=True, blank=True)
    wallet_address = models.CharField(max_length=254, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    #objects = UserManager()
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []
    #backend = 'authentication.mybackend.ModelBackend'

    def img(self):
        return format_html("<img width=30 src='{}'>".format(self.photo.url))

    def flag(self):
        return format_html("<img width=30 src='{}'>".format(self.country.flag.url))

    def __str__(self):
        return str(self.username)











#End
