from rest_framework import serializers
from .models import User, Countries





class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=254, allow_null=False)
    password = serializers.CharField(max_length=254, allow_null=False)








class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ('id' ,'name', 'available', 'flag')







class RegisterSerializer(serializers.ModelSerializer):
    #country = serializers.RelatedField(read_only=True)
    #country = CountriesSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'country', 'referral')








class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id' ,'username', 'first_name', 'last_name', 'email', 'is_confirmed', 'referral', 'shop', 'birthday', 'country', 'photo', 'gender', 'wallet_address' )








class ConfirmationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=5, allow_null=False)










#End
