from django.urls import path, include
from . import views



urlpatterns = [
    path('top/', views.Top.as_view(), name='top'),
    path('features/', views.Features.as_view(), name='features'),
    path('description/', views.Description.as_view(), name='description'),
    path('banners/', views.Banners.as_view(), name='banners'),
    path('mobile_banners/', views.MobileBanners.as_view(), name='mobile_banners'),
    path('footer/', views.Footer.as_view(), name='footer'),
]
