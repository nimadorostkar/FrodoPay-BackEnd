from django.urls import path
from authentication import views



urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout, name='logout'),
    path('register', views.Register.as_view(), name='register'),
]
