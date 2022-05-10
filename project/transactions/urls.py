from django.urls import path
from wallet import views



urlpatterns = [
    path('wallets', views.Wallets.as_view(), name='wallets'),
]
