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


    @receiver(post_save, sender=Payment)
    def post_save(sender, instance, created, **kwargs):
        if not created:
            if instance.status == "PAID":
                user = User.objects.get(email=instance.buyer_email)
                deposit = Transaction(source="coinpayments", destination=user.username, type='deposit', status='success', amount=instance.amount_paid, description='deposit from coinpayments, payment:{}, provider_tx:{}'.format(instance.id,instance.provider_tx))
                deposit.save()
                user.inventory += instance.amount
                user.save()
