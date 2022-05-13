from django.urls import path
from transactions import views



urlpatterns = [
    path('transactions', views.Transactions.as_view(), name='transactions'),
    path('mytransactions', views.Mytransactions.as_view(), name='mytransactions'),
    # coinpayment
    path('payments', views.PaymentList.as_view(), name='payment_list'),
    # transaction
    path('deposit', views.Deposit.as_view(), name='deposit'),
    #
    path('new_transfer', views.Transfer.as_view(), name='transfer'),
    path('confirm_transfer', views.ConfirmTransfer.as_view(), name='confirm_transfer'),
    #path('product/<int:id>', ProductItem.as_view(), name='product_item'),
    #
    path('withdrawal', views.Withdrawal.as_view(), name='withdrawal'),
]
