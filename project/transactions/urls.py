from django.urls import path
from transactions import views



urlpatterns = [
    path('transactions', views.Transactions.as_view(), name='transactions'),
    path('mytransactions', views.Mytransactions.as_view(), name='mytransactions'),
    path('new_transfer', views.Transfer.as_view(), name='new_transfer'),
    path('confirm_transfer/<int:id>', views.ConfirmTransfer.as_view(), name='confirm_transfer'),
    path('withdrawal_req', views.Withdrawal.as_view(), name='withdrawal_req'),
    path('deposit', views.Deposit.as_view(), name='deposit'),
    # coinpayment
    path('payments', views.PaymentList.as_view(), name='payment_list'),
]
