from django.contrib.auth.models import User
from .models import Profile
from django.http import JsonResponse




def index(request):
    profile = Profile.objects.get(user=request.user)
    return JsonResponse({ 'user':request.user.username, 'birthday':profile.birthday, 'img':profile.photo.url })
