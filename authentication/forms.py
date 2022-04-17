from django import forms
from . import models


class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['mobile', ]
