from .models import User
from django.http import JsonResponse
from .serializers import LoginSerializer
from . import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response

from django.contrib.auth import login, authenticate, logout, update_session_auth_hash

from rest_framework.authtoken.models import Token




#------------------------------------------------------- Login ---------------
class Login(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        try:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            print('API Auth Token: ', token.key)
            print('Created New Token:', created)
            user_data={"id":user.id, "first_name":user.first_name, "last_name":user.last_name, "image":user.photo.url, "token": token.key}
            return Response(user_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response('کاربری با شماره {} یافت نشد، لطفا ثبت نام کنید'.format(data['username']) , status=status.HTTP_400_BAD_REQUEST)










'''

# ------------------------------------------------------- Users ---------------

class Users(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    #filterset_fields = ['is_legal', 'is_active', 'is_superuser', 'is_staff']
    #search_fields = ['first_name', 'last_name', 'email', 'mobile', 'company', 'address']
    search_fields = ['shop', 'birthday', 'referral', 'photo']
    #ordering_fields = ['date_joined', 'otp_create_time', 'last_login', 'id']

    def get(self, request, format=None):
        queryset = User.objects.all()
        query = self.filter_queryset(User.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = UsersSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
