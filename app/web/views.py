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
from .serializers import TopSerializer
from . import models







# -------------------------------------------------------------- Top -----------
class Top(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            top = models.Top.objects.get(id=1)
            serializer = TopSerializer(top)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)













# ---------------------------------------------------------- AAAAAAAA ----------
class AAAAAAAA(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            score = UserScore.objects.get(user=request.user)
            data = {'user_score':score.score, 'banner':banner}
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)










# ---------------------------------------------------------- AAAAAAAA ----------
class AAAAAAAA(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            score = UserScore.objects.get(user=request.user)
            data = {'user_score':score.score, 'banner':banner}
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)













#End
