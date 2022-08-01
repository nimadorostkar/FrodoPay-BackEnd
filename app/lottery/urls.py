from django.urls import path
from . import views



urlpatterns = [
    path('lottery', views.Lottery.as_view(), name='lottery'),
    path('det_winners', views.Winners.as_view(), name='winners'),
    path('app_winn_prizes', views.AppWinnPrizes.as_view(), name='app_winn_prizes'),
]
