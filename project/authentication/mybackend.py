from django.contrib.auth.backends import ModelBackend
from .models import User


class Backend(ModelBackend):

    def authenticate(self, request, email, password, **kwargs):
        email = kwargs['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
