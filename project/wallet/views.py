from .models import Wallet
from authentication.models import User
from django.http import JsonResponse
from .serializers import WalletSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404






#--------------------------------------------------------- Wallets ------------
class Wallets(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['inventory', 'updated_at', 'created_at']
    search_fields = ['user__email', 'user__username', 'wallet_id']
    ordering_fields = ['created_at', 'updated_at', 'inventory']

    def get(self, request, format=None):
        query = self.filter_queryset(Wallet.objects.all())
        serializer = WalletSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)













#End
