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
from django_coinpayments.models import Payment
from django_coinpayments.exceptions import CoinPaymentsProviderError
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import pagination
import json
from datetime import datetime, timedelta
from coinpayments import CoinPaymentsAPI




class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100













#----------------------------------------------------- Transaction -------------
class Transactions(GenericAPIView):
    permission_classes = [IsAuthenticated]
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












#-----------------------------------------------------user transactions --------
class UsertransHistory(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    pagination_class = CustomPagination
    queryset = Transaction.objects.filter()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'type', 'created_at']
    search_fields = ['source', 'destination', 'description']
    ordering_fields = ['created_at', 'fee', 'amount']

    def get(self, request, format=None):

        if request.GET.get('date'):
            if request.GET.get('date') == 'past_7_days':
                query = self.filter_queryset(Transaction.objects.filter(Q(destination=request.user.username) | Q(source=request.user.username), created_at__gte=datetime.now()-timedelta(days=7) ).order_by('-created_at') )
            elif request.GET.get('date') == 'this_month':
                query = self.filter_queryset(Transaction.objects.filter(Q(destination=request.user.username) | Q(source=request.user.username), created_at__gte=datetime.now()-timedelta(days=30) ).order_by('-created_at') )
            elif request.GET.get('date') == 'today':
                query = self.filter_queryset(Transaction.objects.filter(Q(destination=request.user.username) | Q(source=request.user.username), created_at__gte=datetime.now()-timedelta(days=1) ).order_by('-created_at') )
            else:
                query = self.filter_queryset(Transaction.objects.filter(Q(destination=request.user.username) | Q(source=request.user.username) ).order_by('-created_at') )
        else:
            query = self.filter_queryset(Transaction.objects.filter(Q(destination=request.user.username) | Q(source=request.user.username) ).order_by('-created_at') )

        page = self.paginate_queryset(query)
        if page is not None:
            serializer = TransactionSerializer(page, many=True)
            transactions = []
            for obj in serializer.data:
                trans_status = 'unknown'
                if obj['type'] == 'transfer' and obj['source'] == request.user.username:
                    trans_status = 'transfer_withdrawal'
                elif obj['type'] == 'transfer' and obj['destination'] == request.user.username:
                    trans_status = 'transfer_deposit'
                elif obj['type'] == 'withdrawal':
                    trans_status = 'withdrawal'
                elif obj['type'] == 'deposit':
                    trans_status = 'deposit'
                trans = { 'trans_status':trans_status, 'id':obj['id'], 'source':obj['source'], 'destination':obj['destination'], 'amount':obj['amount'],
                          'type':obj['type'], 'status':obj['status'], 'description':obj['description'], 'fee':obj['fee'], 'created_at':obj['created_at'] }
                transactions.append(trans)
            return self.get_paginated_response(transactions)

        serializer = TransactionSerializer(query, many=True)
        transactions = []
        for obj in serializer.data:
            trans_status = 'unknown'
            if obj['type'] == 'transfer' and obj['source'] == request.user.username:
                trans_status = 'transfer_withdrawal'
            elif obj['type'] == 'transfer' and obj['destination'] == request.user.username:
                trans_status = 'transfer_deposit'
            elif obj['type'] == 'withdrawal':
                trans_status = 'withdrawal'
            elif obj['type'] == 'deposit':
                trans_status = 'deposit'
            trans = { 'trans_status':trans_status, 'id':obj['id'], 'source':obj['source'], 'destination':obj['destination'], 'amount':obj['amount'],
                      'type':obj['type'], 'status':obj['status'], 'description':obj['description'], 'fee':obj['fee'], 'created_at':obj['created_at'] }
            transactions.append(trans)
        return Response(transactions, status=status.HTTP_200_OK)
















#----------------------------------------------------------- Transfer ----------
class Transfer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        amount = request.data['amount']
        fee = 0.02
        fee_amount = amount*fee
        total_amount = amount+fee_amount

        transfer = Transaction()
        transfer.type = 'transfer'
        transfer.source = request.user.username

        if request.data['destination'] == request.user.username:
            return Response("Transfer to your account is not possible", status=status.HTTP_400_BAD_REQUEST)

        try:
            destination = User.objects.get(username=request.data['destination'])
            transfer.destination = destination.username
        except:
            return Response("Destination wallet address isn't valid", status=status.HTTP_400_BAD_REQUEST)

        if total_amount <= request.user.inventory:
            transfer.amount = amount
        else:
            return Response("Your inventory is not enough", status=status.HTTP_400_BAD_REQUEST)

        transfer.description = request.data['description']
        transfer.fee = fee_amount
        transfer.status = 'pending'
        transfer.save()

        transfer_data = { 'transfer_id':transfer.id, 'amount':transfer.amount, 'destination':transfer.destination, 'destination_photo':destination.photo.url,
                          'fee':transfer.fee, 'total_amount':total_amount, 'description':transfer.description, 'status':transfer.status }

        return Response(transfer_data, status=status.HTTP_200_OK)








#--------------------------------------------------- Confirm Transfer ----------
class ConfirmTransfer(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            transfer = Transaction.objects.get(id=self.kwargs["id"])

            if transfer.source != request.user.username:
                return Response("You don't have access to this transfer", status=status.HTTP_400_BAD_REQUEST)

            if transfer.status == 'pending':
                try:
                    total_amount = transfer.amount+transfer.fee

                    source = User.objects.get(username=transfer.source)
                    destination = User.objects.get(username=transfer.destination)

                    source.inventory = source.inventory - total_amount
                    source.save()
                    destination.inventory = destination.inventory + transfer.amount
                    destination.save()

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
        amount = request.data['amount']
        fee = 0.02
        fee_amount = amount*fee
        total_amount = amount+fee_amount

        withdrawal = Transaction()
        withdrawal.type = 'withdrawal'
        withdrawal.source = request.user.username

        if request.user.wallet_address == None:
            return Response("Wallet address is empty. Please complete your profile information", status=status.HTTP_400_BAD_REQUEST)
        else:
            withdrawal.destination = request.user.wallet_address

        if total_amount <= request.user.inventory:
            withdrawal.amount = amount
        else:
            return Response("Your inventory is not enough", status=status.HTTP_400_BAD_REQUEST)

        withdrawal.description = request.data['description']
        withdrawal.fee = fee_amount
        withdrawal.status = 'pending'
        withdrawal.save()

        withdrawal_data = { 'withdrawal_id':withdrawal.id, 'amount':withdrawal.amount, 'wallet_address':withdrawal.destination, 'fee':withdrawal.fee,
                            'description':withdrawal.description, 'status':withdrawal.status, 'total_amount':total_amount }

        return Response(withdrawal_data, status=status.HTTP_200_OK)

















#----------------------------------------------------------- Deposit -----------
class Deposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        amount = request.data['amount']
        fee = 0.02
        fee_amount = amount*fee
        total_amount = amount+fee_amount

        deposit = Transaction()
        deposit.type = 'deposit'
        deposit.source = 'coinpayment address'
        deposit.destination = request.user.username
        deposit.amount = amount
        deposit.description = request.data['description']
        deposit.fee = fee_amount
        deposit.status = 'pending'
        deposit.save()

        deposit_data = { 'amount':deposit.amount, 'fee':deposit.fee, 'total_amount':total_amount,
                         'description':deposit.description, 'status':deposit.status, 'withdrawal_id':deposit.id }

        return Response(deposit_data, status=status.HTTP_200_OK)





#----------------------------------------------------------- Deposit -----------
class Coinpay(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        api = CoinPaymentsAPI(public_key='b5ab7e069860af7711a209cf1aa3343d330b155643f231189477a1731aaa87ad', private_key='fcF29cad06dd9900980d3b4221ab7d7afdDF26c9B521337295a43cBDcdd7535B')

        a = api.rates()
        b = api.check_signature('ipn_message', 'ipn signautre')

        params = { 'amount':10, 'currency1':'USD', 'currency2':'BTC' }
        amount = 22
        cc = api.create_transaction()

        #zz = CryptoPayments().getBasicInfo()

        print('-------------')
        print(cc)

        #payment = get_object_or_404(Payment, pk=pk)
        #create_tx(request, payment)

        tx = payment.create_tx()
        payment.status = Payment.PAYMENT_STATUS_PENDING
        payment.save()

        return Response( cc , status=status.HTTP_200_OK)







#----------------------------------------------------- PaymentList -------------
class PaymentList(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):

        payments = Payment.objects.all().values()
        return Response(payments, status=status.HTTP_200_OK)
























#
