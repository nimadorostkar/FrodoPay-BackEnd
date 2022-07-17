from .models import Advertise
from django.http import JsonResponse
from .serializers import AdvertiseSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect













#------------------------------------------------------ Advertise -------------
class Advertise(APIView):
    serializer_class = AdvertiseSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        ad = Advertise.objects.all()
        serializer = AdvertiseSerializer(ad, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)












#End
