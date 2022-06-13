from django.urls import path, include
from transactions import views



urlpatterns = [
    path('transactions', views.Transactions.as_view(), name='transactions'),
    path('trans_history', views.UsertransHistory.as_view(), name='trans_history'),
    path('new_transfer', views.Transfer.as_view(), name='new_transfer'),
    path('confirm_transfer/<int:id>', views.ConfirmTransfer.as_view(), name='confirm_transfer'),
    path('withdrawal_req', views.Withdrawal.as_view(), name='withdrawal_req'),

    # coinpayments
    path('', include('django_coinpayments.urls', namespace='django_coinpayments')),
    path('payment_setup/', views.PaymentSetupView.as_view(), name='payment_setup'),
    path('payments/', views.PaymentList.as_view(), name='payment_list'),
    path('payments/<pk>', views.PaymentDetail.as_view(), name='payment_detail'),
    path('payments/new/<pk>', views.create_new_payment, name='payment_new'),

    #path('new_deposit', views.NewDeposit.as_view(), name='new_deposit'),
    #path('deposit', views.Deposit.as_view(), name='deposit'),
    #path('payments', views.PaymentList.as_view(), name='payment_list'),
    #path('coinpay', views.Coinpay.as_view(), name='coinpay'),
]
