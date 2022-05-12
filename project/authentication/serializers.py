from rest_framework import serializers
from .models import User





class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=254, allow_null=False)
    password = serializers.CharField(max_length=254, allow_null=False)






class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email' ,'username', 'password', 'referral')







class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id' ,'username', 'first_name', 'last_name', 'email', 'is_confirmed', 'referral', 'shop', 'birthday', 'photo', 'gender', 'wallet_address' )









class ConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5, allow_null=False)










#End
