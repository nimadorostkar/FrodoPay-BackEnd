from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save









#------------------------------------------------------------------------------
class Top(models.Model):
    slogan_text = models.CharField(max_length=256, null=True, blank=True)
    buttonText_text = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return str('Top Info')

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)











#------------------------------------------------------------------------------
class Features(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='web/Features')


    def __str__(self):
        return str(self.title)











#------------------------------------------------------------------------------
class Description(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='web/descriptions')
    button_title = models.CharField(max_length=256, null=True, blank=True)
    button_link = models.CharField(max_length=256, null=True, blank=True)


    def __str__(self):
        return str(self.title)














#------------------------------------------------------------------------------
class Banners(models.Model):
    image = models.ImageField(upload_to='web/banners')
    link = models.CharField(max_length=256, null=True, blank=True)


    def __str__(self):
        return str(self.link)











#------------------------------------------------------------------------------
class MobileBanners(models.Model):
    image = models.ImageField(upload_to='web/mobilebanners')
    link = models.CharField(max_length=256, null=True, blank=True)


    def __str__(self):
        return str(self.link)










#------------------------------------------------------------------------------
class Footer(models.Model):
    copyright_text = models.CharField(max_length=256, null=True, blank=True)
    slogan_text = models.CharField(max_length=256, null=True, blank=True)
    instagram_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    instagram_link = models.CharField(max_length=256, null=True, blank=True)
    linkedin_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    linkedin_link = models.CharField(max_length=256, null=True, blank=True)
    youtube_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    youtube_link = models.CharField(max_length=256, null=True, blank=True)
    facebook_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    facebook_link = models.CharField(max_length=256, null=True, blank=True)
    medium_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    medium_link = models.CharField(max_length=256, null=True, blank=True)
    whatsapp_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    whatsapp_link = models.CharField(max_length=256, null=True, blank=True)
    discord_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    discord_link = models.CharField(max_length=256, null=True, blank=True)
    reddit_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    reddit_link = models.CharField(max_length=256, null=True, blank=True)
    telegram_image = models.ImageField(upload_to='web/footer/socials', default='web/footer/socials/default.png', null=True, blank=True)
    telegram_link = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return str('Footer Info')

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)























#End
