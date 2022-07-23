from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from lottery.models import Banner, UserScore, GetScore
#from .serializers import TransactionSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from .models import Banner, UserScore, GetScore
from django.db.models import Q
from random import randint







# ----------------------------------------------------------- Lottery ----------
class Lottery(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            banner = Banner.objects.get(id=1)
            banner_data = {'banner_title:':banner.title, 'banner_img:':banner.img.url}

            score = UserScore.objects.get(user=request.user)

            data = {'banner_data':banner_data, 'user_score':score.score}

            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)













#End
