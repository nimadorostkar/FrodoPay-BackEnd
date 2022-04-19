from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Profile

from django.http import JsonResponse





def index(request):
    profile = Profile.objects.get(user=request.user)
    return JsonResponse({ 'user':request.user.username, 'img':profile.photo.url })
