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
    body = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to='lottery/banner')
    link = models.CharField(max_length=256, null=True, blank=True)

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











#------------------------------------------------------------------------------
class Winner(models.Model):
    winners_qty = models.IntegerField(default=0)
    bonus_amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return 'winners_qty: '+str(self.winners_qty) +'|'+ 'bonus_amount: '+str(self.bonus_amount)

    class Meta:
        verbose_name = "Winners setting"
        verbose_name_plural = "Winners settings"









#------------------------------------------------------------------------------
class WinnersList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def img(self):
        return format_html("<img width=30 src='{}'>".format(self.user.photo.url))

    def __str__(self):
        return str(self.user)











#End
