from django.db import models
from django.contrib.auth.models import AbstractUser
#from authentication.myusermanager import UserManager
from django.utils.html import format_html
from shortuuid.django_fields import ShortUUIDField





#------------------------------------------------------------------------------
class Countries(models.Model):
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=256, unique=True)
    abbreviation = models.CharField(max_length=256, null=True, blank=True, unique=True)
    flag = models.ImageField(upload_to='countries/flag', default='countries/flag/unknown.png')

    def flagImg(self):
        return format_html("<img width=30 src='{}'>".format(self.flag.url))

    def __str__(self):
        return str(self.name)








#------------------------------------------------------------------------------
class User(AbstractUser):
    email = models.EmailField(max_length=256, unique=True)
    shop = models.CharField(max_length=256, null=True, blank=True)
    birthday = models.DateField(max_length=256, null=True, blank=True)
    country = models.ForeignKey(Countries, null=True, blank=True , on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user/photo',default='user/photo/default.png', null=True, blank=True)
    CHOICES = ( ('male','male'), ('female','female'), ('unspecified','unspecified') )
    gender = models.CharField(max_length=256, default='unspecified', choices=CHOICES, null=True, blank=True)
    referral = models.CharField(max_length=256, null=True, blank=True)
    wallet_address = models.CharField(max_length=256, null=True, blank=True)
    conf_code = models.IntegerField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    inventory = models.DecimalField(max_digits=30, decimal_places=5, default=0)
    invitation_referral = ShortUUIDField(length=8, max_length=15, alphabet="abcdefg1234", editable=False)

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
















#------------------------------------------------------------------------------
class NotifLists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    body = models.CharField(max_length=256, null=True, blank=True)
    CHOICES = ( ('TRANSFER','TRANSFER'), ('DEPOSIT','DEPOSIT'), ('WITHDRAWAL','WITHDRAWAL'), ('USER','USER'), ('DEFAULT','DEFAULT') )
    type = models.CharField(max_length=256, default='DEFAULT', choices=CHOICES)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.title)





#End
