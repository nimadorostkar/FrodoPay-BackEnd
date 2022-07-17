from django.urls import path, include
from advertise import views




urlpatterns = [
    path('advertise', views.Advertise.as_view(), name='advertise'),
]
