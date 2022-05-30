from django.urls import path
from authentication import views



urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    #path('logout', views.Logout, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('user/<str:username>/', views.User.as_view(), name='user'),
    path('activation/', views.Activation.as_view(), name='activation'),
    path('confirmation/', views.Confirmation.as_view(), name='confirmation'),
    path('countries/', views.Countries.as_view(), name='Countries'),
    path('users/', views.Users.as_view(), name='users'),
    path('usernames/', views.Usernames.as_view(), name='usernames'),
]
