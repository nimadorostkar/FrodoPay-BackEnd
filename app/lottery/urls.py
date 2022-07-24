from django.urls import path
from . import views



urlpatterns = [
    path('lottery', views.Lottery.as_view(), name='lottery'),
    path('winners', views.Winners.as_view(), name='winners'),
]
