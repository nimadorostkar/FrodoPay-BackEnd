from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.myusermanager import UserManager





class User(AbstractUser):
    #username = None
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.CharField(max_length=11, unique=True, verbose_name = "شماره موبایل")
    otp = models.PositiveIntegerField(blank=True, null=True, verbose_name = "کد ورود")
    otp_create_time = models.DateTimeField(auto_now=True, verbose_name = "تاریخ ایجاد کد")
    is_legal = models.BooleanField(default=False, verbose_name = "شخصیت حقوقی")
    company = models.CharField(max_length=80, null=True, blank=True, verbose_name = "نام شرکت")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name = "آدرس")
    email_verification = models.BooleanField(default=False, verbose_name = "تایید ایمیل")
    referral_code = models.CharField(max_length=20, null=True, blank=True, verbose_name = "کد معرف")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    backend = 'authentication.mybackend.ModelBackend'
