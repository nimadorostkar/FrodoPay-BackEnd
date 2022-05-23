from .models import User, Countries
from . import models
from wallet.models import Wallet
from django.http import JsonResponse
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, ConfirmationSerializer, CountriesSerializer
from . import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
import coinaddrvalidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError




#------------------------------------------------------- Login ----------------
class Login(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)
        try:
            user = authenticate(request, username=data['username'], password=data['password'])
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print('API Auth Token: ', token.key)
            print('Created New Token:', created)

            wallet = Wallet.objects.get(user=user)
            user_data = { "id":user.id, "username":user.username, "email":user.email, 'is_confirmed':user.is_confirmed, "first_name":user.first_name,
                          "last_name":user.last_name, "image":user.photo.url, "token": token.key, "wallet_id":wallet.wallet_id,
                          "inventory":wallet.inventory }

            return Response(user_data, status=status.HTTP_200_OK)
        except:
            return Response('username or password is incorrect', status=status.HTTP_401_UNAUTHORIZED)











#--------------------------------------------------------- logout -------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def Logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully', status=status.HTTP_401_UNAUTHORIZED)















#------------------------------------------------------- Register -------------

class Register(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)
        try:
            validate_password(serializer.data['password'])
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'], country=data['country'], referral=data['referral'])
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        print('API Auth Token: ', token.key)
        print('Created New Token:', created)
        wallet = Wallet()
        wallet.user = user
        wallet.inventory = 0
        wallet.save()
        user_data = { "id":user.id, "username":user.username, "email":user.email, "first_name":user.first_name,
                      "last_name":user.last_name, "image":user.photo.url, "token": token.key, "wallet_id":wallet.wallet_id,
                      "inventory":wallet.inventory }
        return Response(user_data, status=status.HTTP_200_OK)















#-------------------------------------------------------- Profile -------------

class Profile(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        #serializer = UserSerializer(profile)
        wallet = Wallet.objects.get(user=profile)
        data = {
                'id':profile.id, 'username':profile.username, 'first_name':profile.first_name,
                'last_name':profile.last_name, 'email':profile.email, 'is_confirmed':profile.is_confirmed, 'referral':profile.referral,
                'shop':profile.shop, 'photo':profile.photo.url, 'gender':profile.gender,
                'birthday':profile.birthday, 'country':profile.country.name, 'wallet_address':profile.wallet_address,
                'last_login':profile.last_login, 'wallet_id':wallet.wallet_id, 'inventory':wallet.inventory
                }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        data=request.data
        data['email'] = profile.email
        addr = coinaddrvalidator.validate('eth', data['wallet_address'])
        if addr.valid:
            serializer = UserSerializer(profile, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response('Wallet address is not valid',status=status.HTTP_406_NOT_ACCEPTABLE)


    def delete(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def post(self, request, *args, **kwargs):
        try:
            file = request.data['file']
        except KeyError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        profile = get_object_or_404(User, id=self.request.user.id)
        profile.photo = file
        profile.save()
        data = {"image":profile.image.url}
        return Response(data, status=status.HTTP_200_OK)









#------------------------------------------------------ Activation -------------

class Activation(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = User.objects.get(id=self.request.user.id)
        # send activation email
        code="12345"
        print("-----------------")
        print("Email activation code is: {}".format(code))
        return Response("Activation code send to {}".format(profile.email) , status=status.HTTP_200_OK)








#------------------------------------------------------ Confirmation -----------

class Confirmation(APIView):
    serializer_class = ConfirmationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)

        profile = User.objects.get(id=self.request.user.id)
        if data['code'] == '12345':
            profile.is_confirmed = True
            profile.save()
            return Response("User verified", status=status.HTTP_200_OK)
        else:
            return Response("User not verified", status=status.HTTP_406_NOT_ACCEPTABLE)














#------------------------------------------------------ Activation -------------

class Countries(APIView):
    serializer_class = CountriesSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        countries = models.Countries.objects.filter(available=True)
        serializer = CountriesSerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)











#End
