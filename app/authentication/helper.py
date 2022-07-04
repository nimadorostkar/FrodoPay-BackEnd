from core import settings
from rest_framework.response import Response
from rest_framework import status
from random import randint
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
import datetime
import time
import random
import string
import json






def random_code():
    return  randint(10000, 99999)







def send_code(profile, code):
    subject = 'FrodoPay activation code'
    message = f'Hi {profile.username}, Thank you for using our service. Your activation code is: {code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [profile.email, ]
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return 0
            #return HttpResponse('Invalid header found.')
        return 1
        #return HttpResponseRedirect('/contact/thanks/')
    else:
        return 0
        #return HttpResponse('Make sure all fields are entered and valid.')





'''
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
'''













#End
