from django.urls import path
from transactions import views



urlpatterns = [
    path('transactions', views.Transactions.as_view(), name='transactions'),
    path('mytransactions', views.Mytransactions.as_view(), name='mytransactions'),
    # coinpayment
    path('payments', views.PaymentList.as_view(), name='payment_list'),
    # transaction
    path('deposit', views.Deposit.as_view(), name='deposit'),
    path('transfer', views.Transfer.as_view(), name='transfer'),
    path('withdrawal', views.Withdrawal.as_view(), name='withdrawal'),
]
