from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .models import Top, Features, Description, Banners, MobileBanners, Footer
from .serializers import TopSerializer, FeaturesSerializer, DescriptionSerializer, BannersSerializer, MobileBannersSerializer, FooterSerializer
from . import models







#-------------------------------------------------------------- Top ------------
class Top(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            top = models.Top.objects.get(id=1)
            serializer = TopSerializer(top)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)














#--------------------------------------------------------- Features ------------
class Features(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            features = models.Features.objects.all()
            serializer = FeaturesSerializer(features, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)














#------------------------------------------------------ Description ------------
class Description(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            description = models.Description.objects.all()
            serializer = DescriptionSerializer(description, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)







#---------------------------------------------------------- Banners ------------
class Banners(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            banners = models.Banners.objects.all()
            serializer = BannersSerializer(banners, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)













#---------------------------------------------------- MobileBanners ------------
class MobileBanners(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            mobilebanners = models.MobileBanners.objects.all()
            serializer = MobileBannersSerializer(mobilebanners, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)









#----------------------------------------------------------- Footer ------------
class Footer(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            footer = models.Footer.objects.get(id=1)
            serializer = FooterSerializer(footer)
            social = {
             'instagram_image': serializer.data['instagram_image'],
             'instagram_link': serializer.data['instagram_link'],
             'linkedin_image': serializer.data['linkedin_image'],
             'linkedin_link': serializer.data['linkedin_link'],
             'youtube_image': serializer.data['youtube_image'],
             'youtube_link': serializer.data['youtube_link'],
             'facebook_image': serializer.data['facebook_image'],
             'facebook_link': serializer.data['facebook_link'],
             'medium_image': serializer.data['medium_image'],
             'medium_link': serializer.data['medium_link'],
             'whatsapp_image': serializer.data['whatsapp_image'],
             'whatsapp_link': serializer.data['whatsapp_link'],
             'discord_image': serializer.data['discord_image'],
             'discord_link': serializer.data['discord_link'],
             'reddit_image': serializer.data['reddit_image'],
             'reddit_link': serializer.data['reddit_link'],
             'telegram_image': serializer.data['telegram_image'],
             'telegram_link': serializer.data['telegram_link']
            }
            data = { 'copyright_text':serializer.data['copyright_text'], 'slogan_text':serializer.data['slogan_text'], 'social':social }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)











#End
