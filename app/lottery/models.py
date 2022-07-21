from django.db import models
from django.urls import reverse
from authentication.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_coinpayments.models import Payment
from django.utils.html import format_html






#------------------------------------------------------------------------------
class Banner(models.Model):
    title = models.CharField(max_length=256)
    img = models.ImageField(upload_to='lottery/banner')

    def BannerImg(self):
        return format_html("<img width=30 src='{}'>".format(self.img.url))

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)









#------------------------------------------------------------------------------
class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + '|' + str(self.score)









#------------------------------------------------------------------------------
class GetScore(models.Model):
    invite = models.IntegerField(default=0)
    deposit = models.IntegerField(default=0)
    register = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)


    def __str__(self):
        return 'invite_score: '+str(self.invite) +'|'+ 'deposit_score: '+str(self.deposit) +'|'+ 'register_score: '+str(self.register)











#End
