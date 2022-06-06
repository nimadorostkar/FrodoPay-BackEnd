from core import settings
from rest_framework.response import Response
from rest_framework import status
from random import randint
from django.core.mail import send_mail
import datetime
import time
import random
import string
import json






def random_code():
    return  randint(100000, 999999)





def send_code(profile, code):
    try:
        subject = 'FrodoPay activation code'
        message = f'Hi {profile.username}, Thank you for using our service. Your activation code is: {code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [profile.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return 1
    except:
        return 0














#End
