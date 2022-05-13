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
class Transfer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        mywallet = Wallet.objects.get(user=request.user)
        amount = request.data['amount']
        fee = 0.02
        fee_amount = amount*fee
        total_amount = amount+fee_amount

        transfer = Transaction()
        transfer.type = 'transfer'
        transfer.source = mywallet.wallet_id

        try:
            destination = Wallet.objects.get(wallet_id=request.data['destination'])
            transfer.destination = destination.wallet_id
        except:
            return Response("Destination wallet address isn't valid", status=status.HTTP_400_BAD_REQUEST)

        if total_amount <= mywallet.inventory:
            transfer.amount = amount
        else:
            return Response("Your inventory is not enough", status=status.HTTP_400_BAD_REQUEST)

        transfer.description = request.data['description']
        transfer.fee = fee_amount
        transfer.status = 'pending'
        transfer.save()

        transfer_data = { 'amount':transfer.amount, 'destination_wallet_id':transfer.destination, 'destination_username':destination.user.username,
                          'destination_photo':destination.user.photo.url, 'fee':transfer.fee, 'total_amount':total_amount,
                          'description':transfer.description, 'status':transfer.status, 'transfer_id':transfer.id }

        return Response(transfer_data, status=status.HTTP_200_OK)






#--------------------------------------------------- Confirm Transfer ----------
class ConfirmTransfer(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            transfer = Transaction.objects.get(id=self.kwargs["id"])
            if transfer.status == 'pending':
                try:
                    total_amount = transfer.amount+transfer.fee

                    source_wallet = Wallet.objects.get(user=request.user)
                    destination_wallet = Wallet.objects.get(wallet_id=transfer.destination)

                    source_wallet.inventory = source_wallet.inventory - total_amount
                    source_wallet.save()
                    destination_wallet.inventory = destination_wallet.inventory + total_amount
                    destination_wallet.save()

                    transfer.status = 'success'
                    transfer.save()
                    return Response('The transfer was successful', status=status.HTTP_200_OK)
                except:
                    transfer.status = 'fail'
                    transfer.save()
                    return Response("Transfer failed", status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response("This request is invalid", status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response("Transfer request not found", status=status.HTTP_400_BAD_REQUEST)




















#--------------------------------------------------------- Withdrawal ----------
class Withdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        mywallet = Wallet.objects.get(user=request.user)
        amount = request.data['amount']
        fee = 0.02
        fee_amount = amount*fee
        total_amount = amount+fee_amount

        withdrawal = Transaction()
        withdrawal.type = 'withdrawal'
        withdrawal.source = mywallet.wallet_id

        if request.user.wallet_address == None:
            return Response("Wallet address is empty. Please complete your profile information", status=status.HTTP_400_BAD_REQUEST)
        else:
            withdrawal.destination = request.user.wallet_address

        if total_amount <= mywallet.inventory:
            withdrawal.amount = amount
        else:
            return Response("Your inventory is not enough", status=status.HTTP_400_BAD_REQUEST)

        withdrawal.description = request.data['description']
        withdrawal.fee = fee_amount
        withdrawal.status = 'pending'
        withdrawal.save()

        withdrawal_data = { 'amount':withdrawal.amount, 'wallet_address':withdrawal.destination, 'fee':withdrawal.fee,
                            'total_amount':total_amount, 'description':withdrawal.description, 'status':withdrawal.status,
                            'withdrawal_id':withdrawal.id }

        return Response(withdrawal_data, status=status.HTTP_200_OK)

























#----------------------------------------------------------- Deposit -----------
class Deposit(GenericAPIView):
    pass















#
