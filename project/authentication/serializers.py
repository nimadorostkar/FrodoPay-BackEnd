from rest_framework import serializers
from .models import User





class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=254, allow_null=False)
    password = serializers.CharField(max_length=254, allow_null=False)
