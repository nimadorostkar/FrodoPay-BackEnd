from .models import User
from django.http import JsonResponse
from .serializers import LoginSerializer, RegisterSerializer
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
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        print('API Auth Token: ', token.key)
        print('Created New Token:', created)
        user_data={"id":user.id, "first_name":user.first_name, "last_name":user.last_name, "image":user.photo.url, "token": token.key}
        return Response(user_data, status=status.HTTP_200_OK)



















#End
