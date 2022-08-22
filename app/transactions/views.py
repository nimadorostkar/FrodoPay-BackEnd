from django.http import HttpResponseRedirect
from django.urls import reverse
import requests
from django.shortcuts import render, get_object_or_404
from authentication.models import User, NotifLists
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
from .models import Transaction, WithdrawalCeiling
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import pagination
import json
from datetime import datetime, timedelta
from random import randint
from django_coinpayments.models import Payment, CoinPaymentsTransaction
from django_coinpayments.exceptions import CoinPaymentsProviderError
from decimal import Decimal
from django import forms
from fee.models import FeeRates, InputHistory, Inventory

from firebase_admin.messaging import Message, Notification, AndroidNotification
from fcm_django.models import FCMDevice




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












#---------------------------------------------------- user transactions --------
class UsertransHistory(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    pagination_class = CustomPagination
    queryset = Transaction.objects.filter()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'type', 'created_at', 'source', 'destination']
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
                trans = { 'trans_status':trans_status, 'id':obj['id'], 'source':obj['source'], 'destination':obj['destination'], 'amount':obj['amount'], 'normalize_amount':Decimal(obj['amount']).normalize(),
                          'type':obj['type'], 'status':obj['status'], 'description':obj['description'], 'fee':obj['fee'], 'normalize_fee':Decimal(obj['fee']).normalize(), 'created_at':obj['created_at'] }
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
            trans = { 'trans_status':trans_status, 'id':obj['id'], 'source':obj['source'], 'destination':obj['destination'], 'amount':obj['amount'], 'normalize_amount':Decimal(obj['amount']).normalize(),
                      'type':obj['type'], 'status':obj['status'], 'description':obj['description'], 'fee':obj['fee'], 'normalize_fee':Decimal(obj['fee']).normalize(), 'created_at':obj['created_at'] }
            transactions.append(trans)
        return Response(transactions, status=status.HTTP_200_OK)


















#------------------------------------------------------ UsertransChart ---------
class UsertransChart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        if request.GET.get('date'):
            now = datetime.now().date()
            thisyear = int(now.strftime("%Y"))
            thismonth = int(now.strftime("%m"))
            today = int(now.strftime("%d"))

            chart_data=[]

            total_income = sum(Transaction.objects.filter(destination=request.user.username, status='success').values_list('amount', flat=True))
            total_expense = sum(Transaction.objects.filter(source=request.user.username, status='success').values_list('amount', flat=True))
            total_spending = sum(Transaction.objects.filter( Q(source=request.user.username) | Q(destination=request.user.username) , status='success').values_list('amount', flat=True))


            if request.GET.get('date') == 'month':
                for month in [thismonth, thismonth-1, thismonth-2,  thismonth-3,  thismonth-4]:
                    date = "{}-{}".format(thisyear,month)
                    income = sum(Transaction.objects.filter(destination=request.user.username, status='success', created_at__year=thisyear, created_at__month=month ).values_list('amount', flat=True))
                    expense = sum(Transaction.objects.filter(source=request.user.username, status='success', created_at__year=thisyear, created_at__month=month ).values_list('amount', flat=True))
                    month_data = {'date':date, 'income':income, 'expense':expense}
                    chart_data.append(month_data)

            elif request.GET.get('date') == 'day':
                for day in [today, today-1, today-2,  today-3,  today-4]:
                    date = "{}-{}-{}".format(thisyear,thismonth,day)
                    income = sum(Transaction.objects.filter(destination=request.user.username, status='success', created_at__year=thisyear, created_at__month=thismonth, created_at__day=day ).values_list('amount', flat=True))
                    expense = sum(Transaction.objects.filter(source=request.user.username, status='success', created_at__year=thisyear, created_at__month=thismonth, created_at__day=day ).values_list('amount', flat=True))
                    day_data = {'date':date, 'income':income, 'expense':expense}
                    chart_data.append(day_data)

            if request.GET.get('date') == '90day':
                for month in [thismonth, thismonth-1, thismonth-2,  thismonth-3,  thismonth-4]:
                    date = "{}-{}".format(thisyear,month)
                    income = sum(Transaction.objects.filter(destination=request.user.username, status='success', created_at__year=thisyear, created_at__month=month ).values_list('amount', flat=True))
                    expense = sum(Transaction.objects.filter(source=request.user.username, status='success', created_at__year=thisyear, created_at__month=month ).values_list('amount', flat=True))
                    month_data = {'date':date, 'income':income, 'expense':expense}
                    chart_data.append(month_data)

            data = { 'total_spending':total_spending, 'total_income':total_income, 'total_expense':total_expense, 'chart_data':chart_data}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Enter date in params", status=status.HTTP_200_OK)








#----------------------------------------------------------- Transfer ----------
class Transfer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        amount = request.data['amount']
        fee = float(FeeRates.objects.get(id=1).transfer)

        fee_amount = amount*fee
        total_amount = amount+fee_amount

        transfer = Transaction()
        transfer.type = 'transfer'
        transfer.source = request.user.username

        #zzz = Decimal('123.090000')
        #print(zzz.normalize())

        if request.data['destination'] == request.user.username:
            return Response("Transfer to your account is not possible", status=status.HTTP_400_BAD_REQUEST)

        try:
            destination = User.objects.get(is_confirmed=True, username=request.data['destination'])
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
                    feeinput = InputHistory()
                    feeinput.transaction = transfer
                    feeinput.amount = transfer.fee
                    feeinput.save()
                    fee_inventory = Inventory.objects.get(id=1)
                    fee_inventory.amount += transfer.fee
                    fee_inventory.save()
                except Exception as e:
                    print('-------------')
                    print(e)
                    transfer.status = 'fail'
                    transfer.save()
                    return Response("Error in completing the confirmation", status=status.HTTP_400_BAD_REQUEST)

                try:
                    now = datetime.now()
                    destination_user = User.objects.get(username=transfer.destination)
                    device = FCMDevice.objects.filter(user=request.user)
                    device.send_message(Message( data={ "username":request.user.username, "title":"transfer to {}".format(transfer.destination), "body":"transfer {} BUSD to {} was done successfully".format(transfer.amount,transfer.destination), "type":"TRANSFER", "time":str(now) } ))
                    notif = NotifLists()
                    notif.title = "transfer to {}".format(transfer.destination)
                    notif.body = "transfer {} BUSD to {} was done successfully".format(transfer.amount,transfer.destination)
                    notif.type = "TRANSFER"
                    notif.time = now
                    notif.user = request.user
                    notif.save()

                    device2 = FCMDevice.objects.filter(user=destination_user)
                    device2.send_message(Message( data={ "username":destination_user.username, "title":"received from {}".format(transfer.source), "body":"received {} BUSD from {} successfully".format(transfer.amount,transfer.source), "type":"TRANSFER", "time":str(now) } ))
                    notif2 = NotifLists()
                    notif2.title = "received from {}".format(transfer.source)
                    notif2.body = "received {} BUSD from {} successfully".format(transfer.amount,transfer.source)
                    notif2.type = "TRANSFER"
                    notif2.time = now
                    notif2.user = destination_user
                    notif2.save()

                    print("data notification sent successfully" )
                    return Response('The transfer was successful', status=status.HTTP_200_OK)
                except Exception as e:
                    print('-------------')
                    print(e)
                    transfer.status = 'fail'
                    transfer.save()
                    return Response("Error in sending notification", status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response("This request is invalid", status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response("Transfer request not found", status=status.HTTP_400_BAD_REQUEST)











#--------------------------------------------------------- Withdrawal ----------
class Withdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        amount = Decimal(request.data['amount'])
        fee = FeeRates.objects.get(id=1).withdrawal
        fee_amount = amount*fee
        total_amount = amount+fee_amount

        withdrawal = Transaction()
        withdrawal.type = 'withdrawal'
        withdrawal.source = request.user.username

        now = datetime.now().date()
        thisyear = int(now.strftime("%Y"))
        thismonth = int(now.strftime("%m"))
        today = int(now.strftime("%d"))
        ceiling = WithdrawalCeiling.objects.get(id=1)

        daily = sum(Transaction.objects.filter(source=request.user.username,type='withdrawal',status='success', created_at__year=thisyear, created_at__month=thismonth, created_at__day=today ).values_list('amount', flat=True))
        monthly = sum(Transaction.objects.filter(source=request.user.username,type='withdrawal',status='success', created_at__year=thisyear, created_at__month=thismonth ).values_list('amount', flat=True))

        if daily+total_amount >= ceiling.daily:
            return Response("Your daily withdrawal limit is full", status=status.HTTP_400_BAD_REQUEST)
        elif monthly+total_amount >= ceiling.monthly:
            return Response("Your monthly withdrawal limit is full", status=status.HTTP_400_BAD_REQUEST)

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













#--------------------------------------------- WalletConnectDeposit ------------
class WalletConnectDeposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        req = request.data

        txhash = req['txhash']
        user = User.objects.get(username=req['user'])
        amount = req['amount']
        token = req['token']

        bscscan_check = 'https://api.bscscan.com/api?module=transaction&action=gettxreceiptstatus&txhash={}'.format(txhash)
        url_json_data = requests.get(bscscan_check).json()
        dump_data = json.dumps(url_json_data)
        url_data = json.loads(dump_data)
        print(url_data["status"])

        data = { 'data':url_data }
        return Response(data, status=status.HTTP_200_OK)




















#------------------------------------------------------------------------------#
#------------------------------------------------------- Coinpayment ----------#
#------------------------------------------------------------------------------#






def create_tx(request, payment):
    context = {}
    try:
        tx = payment.create_tx()
        payment.status = Payment.PAYMENT_STATUS_PENDING
        payment.save()
        context = { 'id':payment.id, 'currency_original':payment.currency_original, 'currency_paid':payment.currency_paid, 'amount':payment.amount,
                 'amount_paid':payment.amount_paid, 'buyer_email':payment.buyer_email, 'provider_tx_id':payment.provider_tx_id, 'status':payment.status,
                 'created':payment.created, 'modified':payment.modified, 'qrcode_url':payment.provider_tx.qrcode_url, 'status_url':payment.provider_tx.status_url,
                 'address':payment.provider_tx.address, 'timeout':payment.provider_tx.timeout }
        return Response(context, status=status.HTTP_200_OK)
    except CoinPaymentsProviderError as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)









#------------------------------------------------------ PaymentDetail ----------
class PaymentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            object = Payment.objects.get(id=self.kwargs["pk"])
            data = { 'id':object.id, 'currency_original':object.currency_original, 'currency_paid':object.currency_paid, 'amount':object.amount,
                     'amount_paid':object.amount_paid, 'buyer_email':object.buyer_email, 'provider_tx_id':object.provider_tx_id, 'status':object.status,
                     'created':object.created, 'modified':object.modified, 'qrcode_url':object.provider_tx.qrcode_url, 'status_url':object.provider_tx.status_url,
                     'address':object.provider_tx.address, 'timeout':object.provider_tx.timeout }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response("Payment not found", status=status.HTTP_400_BAD_REQUEST)









#---------------------------------------------------- PaymentSetupView ---------
class PaymentSetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        req = request.data

        payment = Payment( currency_original='USDT.TRC20', currency_paid=req['currency_paid'], amount=Decimal(req['amount']),
                           amount_paid=Decimal(0), buyer_email=request.user.email, status=Payment.PAYMENT_STATUS_PROVIDER_PENDING )
        return create_tx(self.request, payment)








#------------------------------------------------------- PaymentList -----------
class PaymentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        obj = Payment.objects.all()
        '''
        data=[]
        for payment in obj:
            paymentdata = {'created':payment.created, 'modified':payment.modified, 'id':payment.id, 'currency_original':payment.currency_original,
                    'currency_paid':payment.currency_paid, 'amount':payment.amount, 'amount_paid':payment.amount_paid, 'buyer_email':payment.buyer_email,
                    'provider_tx_id':payment.provider_tx_id, 'status':payment.status }
            data.append(paymentdata)
        sorteddata= sorted(data, key=attrgetter('created'))
        '''

        return Response(obj.values(), status=status.HTTP_200_OK)








def create_new_payment(self, request, *args, **kwargs):
    payment = get_object_or_404(Payment, pk=self.kwargs["pk"])
    if payment.status in [Payment.PAYMENT_STATUS_PROVIDER_PENDING, Payment.PAYMENT_STATUS_TIMEOUT]:
        pass
    elif payment.status in [Payment.PAYMENT_STATUS_PENDING]:
        payment.provider_tx.delete()
    else:
        return Response("Invalid status - {}".format(payment.get_status_display()), status=status.HTTP_400_BAD_REQUEST)
    return create_tx(request, payment)















#End
