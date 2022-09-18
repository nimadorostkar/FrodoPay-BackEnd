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
from .models import Banner, UserScore, GetScore, Winner, WinnersList
from . import models
from django.db.models import Q
from random import randint
from authentication.models import User
import random







# ----------------------------------------------------------- Lottery ----------
class Lottery(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            score = UserScore.objects.get(user=request.user)
            banner = Banner.objects.all().last()
            list_type = banner.list_display

            if list_type == 'TOP-SCORE':
                list = []
                scores = UserScore.objects.all().order_by('score')[:10]
                for Score in scores:
                    user_score = UserScore.objects.get(user=Score.user)
                    user = {'username':Score.user.username, 'first_name':Score.user.first_name, 'last_name':Score.user.last_name, 'photo':Score.user.photo.url, 'score':user_score.score   }
                    list.append(user)
            elif list_type == 'WINNERS':
                list = []
                winners = WinnersList.objects.all()
                for Winner in winners:
                    user_score = UserScore.objects.get(user=Winner.user)
                    user = {'username':Winner.user.username, 'first_name':Winner.user.first_name, 'last_name':Winner.user.last_name, 'photo':Winner.user.photo.url, 'score':user_score.score   }
                    list.append(user)

            data = {'user_score':score.score, 'banner':banner.img.url, 'link':banner.link, 'body':banner.body, 'title':banner.title, 'list_type':list_type, 'list':list}
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)













# ----------------------------------------------------------- Winners ----------
class Winners(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            winners_data = Winner.objects.get(id=1)
            winners_qty = winners_data.winners_qty     # number of winners
            bonus_amount = winners_data.bonus_amount   # each winner bonus

            all_users = []
            for User in UserScore.objects.all():
                for x in range(User.score):
                    all_users.append(User.user)

            random_items = random.sample(all_users, winners_qty)

            winners_list = WinnersList.objects.all()
            for obj in winners_list:
                obj.delete()

            for winner in random_items:
                if not WinnersList.objects.filter(user=winner):
                    WL = WinnersList()
                    WL.user = winner
                    WL.save()

            return Response('The list of winners has been determined', status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)













#----------------------------------------------------- AppWinnPrizes -----------
class AppWinnPrizes(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            winners_data = models.Winner.objects.get(id=1)
            bonus_amount = winners_data.bonus_amount   # each winner bonus

            for Winner in WinnersList.objects.all():
                user = User.objects.get(username=Winner.user.username)
                user.inventory += bonus_amount
                user.save()

            return Response('The bonus was awarded to the winners', status=status.HTTP_200_OK)
        except:
            return Response('Something went wrong please try again', status=status.HTTP_400_BAD_REQUEST)








#End
