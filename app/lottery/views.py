from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from lottery.models import Banner, UserScore, GetScore, WinnersList
from .serializers import WinnersListSerializer
from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from .models import Banner, UserScore, GetScore, Winner
from django.db.models import Q
from random import randint
from authentication.models import User







# ----------------------------------------------------------- Lottery ----------
class Lottery(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            score = UserScore.objects.get(user=request.user)
            banner = Banner.objects.get(id=1)

            winners_list = []
            winners = WinnersList.objects.all()
            for Winner in winners:
                user_score = UserScore.objects.get(user=Winner.user)
                user = {'username':Winner.user.username, 'fname':Winner.user.first_name, 'lname':Winner.user.last_name, 'user_img':Winner.user.photo.url, 'score':user_score.score   }
                winners_list.append(user)

            data = {'user_score':score.score, 'banner':banner.img.url, 'link':banner.link, 'body':banner.body, 'title':banner.title, 'winners':winners_list}
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)













# ----------------------------------------------------------- Lottery ----------
class Winners(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            winners_data = Winner.objects.get(id=1)
            winners_qty = winners_data.winners_qty     # number of winners
            bonus_amount = winners_data.bonus_amount   # each winner bonus

            all_users = []
            print('------------')
            for User in UserScore.objects.all():
                print(User.user)
                print(User.score)



            #winners = {'1':'nimaaa', '2':'nimaaa2', '3':'nimaaa3', '4':'nimaaa', '5':'nimaaa5', '6':'nimaaa6'}
            data = {'user_score':score.score, 'banner:':banner.img.url, 'body:':banner.body, 'title:':banner.title, 'winners':winners}


            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)









#End
