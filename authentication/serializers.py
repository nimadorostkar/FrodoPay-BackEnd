from rest_framework import serializers
from .models import User




class RequestOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=64, allow_null=False)




class verifyOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=64, allow_null=False)
    otp = serializers.CharField(max_length=4, allow_null=False)




class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'







class registerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mobile' ,'is_legal', 'first_name','last_name', 'company', 'email', 'address')
