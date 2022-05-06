from django.urls import path
from authentication import views



urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout, name='logout'),
    #path('verify', Verify.as_view(), name='verify'),
    #path('logout', Logout, name='logout'),
    #path('register', Register.as_view(), name='register'),
    #path('users', Users.as_view(), name='users'),
    #path('profile', Profile.as_view(), name='profile'),
]
