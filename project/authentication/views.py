from .models import User
from wallet.models import Wallet
from django.http import JsonResponse
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
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
            user_data={"id":user.id, "first_name":user.first_name, "last_name":user.last_name, "image":user.photo.url, "token": token.key}
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
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'], referral=data['referral'])
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        print('API Auth Token: ', token.key)
        print('Created New Token:', created)
        user_data={"id":user.id, "username":user.username, "email":user.email, "first_name":user.first_name, "last_name":user.last_name, "image":user.photo.url, "token": token.key}
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
                'last_name':profile.last_name, 'email':profile.email, 'referral':profile.referral,
                'shop':profile.shop, 'photo':profile.photo.url, 'gender':profile.gender,
                'birthday':profile.birthday, 'wallet_address':profile.wallet_address,
                'last_login':profile.last_login, 'wallet_id':wallet.wallet_id, 'inventory':wallet.inventory
                }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        profile = get_object_or_404(User, id=self.request.user.id)
        serializer = UserSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

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
        return Response(status=status.HTTP_200_OK)


















#End
