from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from authentication.models import User
from .serializers import TransactionSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from django_filters.rest_framework import DjangoFilterBackend
from django.views import generic
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth.signals import user_logged_in
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from .models import Transaction
from wallet.models import Wallet

from django_coinpayments.models import Payment
from django_coinpayments.exceptions import CoinPaymentsProviderError








#----------------------------------------------------- Transaction -------------
class Transactions(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'type']
    search_fields = ['source', 'destination', 'description']
    ordering_fields = ['created_at', 'fee', 'amount']

    def get(self, request, format=None):
        query = self.filter_queryset(Transaction.objects.all())
        serializer = TransactionSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        query = self.filter_queryset(Transaction.objects.all())
        serializer = TransactionSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)











#----------------------------------------------------- Mytransactions ----------
class Mytransactions(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.filter()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'type']
    search_fields = ['source', 'destination', 'description']
    ordering_fields = ['created_at', 'fee', 'amount']

    def get(self, request, format=None):
        try:
            mywallet = Wallet.objects.get(user=request.user)

            inputs = Transaction.objects.filter(destination=mywallet.wallet_id)
            input_query = self.filter_queryset(inputs)
            input_serializer = TransactionSerializer(input_query, many=True)

            outputs = Transaction.objects.filter(source=mywallet.wallet_id)
            output_query = self.filter_queryset(outputs)
            output_serializer = TransactionSerializer(output_query, many=True)

            data = { 'inputs': input_serializer.data, 'outputs': output_serializer.data  }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def post(self, request, format=None):
        query = self.filter_queryset(Transaction.objects.all())
        serializer = TransactionSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)











#----------------------------------------------------- PaymentList -------------
class PaymentList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        payments = Payment.objects.all().values()
        return Response(payments, status=status.HTTP_200_OK)















#----------------------------------------------------------- Transfer ----------
class Transfer(GenericAPIView):
    pass










#----------------------------------------------------------- Deposit -----------
class Deposit(GenericAPIView):
    pass










#--------------------------------------------------------- Withdrawal ----------
class Withdrawal(GenericAPIView):
    pass













#
