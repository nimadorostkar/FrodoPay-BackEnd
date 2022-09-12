from django.urls import path, include
from transactions import views



urlpatterns = [
    path('transactions', views.Transactions.as_view(), name='transactions'),
    path('trans_history', views.UsertransHistory.as_view(), name='trans_history'),
    path('trans_chart', views.UsertransChart.as_view(), name='trans_chart'),
    path('new_transfer', views.Transfer.as_view(), name='new_transfer'),
    path('confirm_transfer/<int:id>', views.ConfirmTransfer.as_view(), name='confirm_transfer'),
    path('withdrawal_req', views.Withdrawal.as_view(), name='withdrawal_req'),
    path('deposit', views.WalletConnectDeposit.as_view(), name='deposit'),
    path('deposit_hash', views.DepositHash.as_view(), name='deposit_hash'),
]
