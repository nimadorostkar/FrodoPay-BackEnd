from django.urls import path
from authentication import views



urlpatterns = [
    #path('', views.index, name="index"),
    path('users', views.Users.as_view(), name='users'),
]
