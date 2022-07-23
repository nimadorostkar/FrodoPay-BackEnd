from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from lottery.models import Lottery
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
            slugs = models.Shop.objects.all().values_list('slug',flat=True)
            return Response(slugs, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)













#End
