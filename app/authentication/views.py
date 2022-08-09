from .models import User, Countries, NotifLists
from . import models
from django.http import JsonResponse
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, ConfirmationSerializer, CountriesSerializer, NotifListsSerializer
from . import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import viewsets, filters, status, pagination, mixins
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.core.mail import send_mail
import coinaddrvalidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.conf import settings
from . import helper
from firebase_admin.messaging import Message, Notification, AndroidNotification
from fcm_django.models import FCMDevice
from datetime import datetime, timedelta
from transactions.models import WithdrawalCeiling, Transaction
from advertise.models import HomeBanners
from lottery.models import UserScore




#------------------------------------------------------- Login ----------------
class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)
        try:
            user = authenticate(request, username=data['username'], password=data['password'])
            login(request, user)
            token = RefreshToken.for_user(user)

            if request.user.is_authenticated:
                if FCMDevice.objects.filter(user=request.user):
                    FCMDevice.objects.filter(user=request.user).delete()
                device = FCMDevice()
                device.user = request.user
                device.name = request.user.username
                device.active = True
                device.registration_id = data['device_token']
                device.device_id = request.user.id
                device.type = data['device_type']
                device.save()

            code = helper.random_code()
            user.conf_code = code
            user.save()
            try:
                helper.send_code(user, code)
                otp_send = True
            except:
                otp_send = False
                #return Response("Error sending OTP email", status=status.HTTP_400_BAD_REQUEST)

            daily_ceiling = WithdrawalCeiling.objects.get(id=1).daily
            monthly_ceiling = WithdrawalCeiling.objects.get(id=1).monthly
            daily_withdraw_ceiling_remains = daily_ceiling-sum(Transaction.objects.filter(source=str(request.user.username), type='withdrawal', status='success', created_at__gte=datetime.now()-timedelta(days=1)).values_list('amount', flat=True) )
            monthly_withdraw_ceiling_remains = monthly_ceiling-sum(Transaction.objects.filter(source=str(request.user.username), type='withdrawal', status='success', created_at__gte=datetime.now()-timedelta(days=30)).values_list('amount', flat=True) )

            token_response = { "refresh": str(token), "access": str(token.access_token) }
            user_response = { "id":user.id, "username":user.username, "email":user.email, 'is_confirmed':user.is_confirmed, 'login':False, "first_name":user.first_name, "otp_send":otp_send,
                          "last_name":user.last_name, "image":user.photo.url, "inventory":user.inventory, "referral":user.referral, "invitation_referral":user.invitation_referral,
                          "daily_withdraw_ceiling_remains":daily_withdraw_ceiling_remains, "monthly_withdraw_ceiling_remains":monthly_withdraw_ceiling_remains }
            response = { 'token':token_response , 'user':user_response }
            return Response(response, status=status.HTTP_200_OK)

        except:
            return Response('username or password is incorrect', status=status.HTTP_406_NOT_ACCEPTABLE)











#--------------------------------------------------------- logout -------------
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(id=request.user.id)
            device = FCMDevice.objects.get(user=user)
            device.delete()
            return Response('User Logged out successfully', status=status.HTTP_200_OK)
        except Exception as e:
            print('-------------')
            print(e)
            return Response('Error in logout', status=status.HTTP_400_BAD_REQUEST)

#request.user.auth_token.delete()
#logout(request)
#request.user.access_token.delete()
#return HttpResponseRedirect('rest_logout')
#return redirect('rest_logout')

#token = RefreshToken.for_user(user)
#access = token.access_token
#token.delete()









#------------------------------------------------------- Register -------------
class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        username_insensitive = models.User.objects.filter(username__iexact=request.data['username']).exclude(email=request.data['email']).exists()  # instead of count, used exists() which does not make any DB query
        if username_insensitive:
            return Response("User with that username already exists.", status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)

        user = models.User.objects.create_user(username=data['username'], email=data['email'], password=data['password'], country=data['country'], referral=data['referral'])
        login(request, user)
        token = RefreshToken.for_user(user)

        code = helper.random_code()
        user.conf_code = code
        user.save()

        referral_user = models.User.objects.filter(invitation_referral=user.referral).first()
        if referral_user:
            referral_user.invited_users += 1
            referral_user.save()


        '''
        if helper.send_code(user, code):
            email_msg = "Activation code send to {}".format(user.email)
        else:
            email_msg = "Error sending email - Please send activation email again!"
        '''
        email_msg = "email service not active"

        if request.user.is_authenticated:
            if FCMDevice.objects.filter(user=request.user):
                FCMDevice.objects.filter(user=request.user).delete()
            device = FCMDevice()
            device.user = request.user
            device.name = request.user.username
            device.active = True
            device.registration_id = data['device_token']
            device.device_id = request.user.id
            device.type = data['device_type']
            device.save()

        user_score = UserScore()
        user_score.user = user
        user_score.score = 1
        user_score.save()

        token_response = { "refresh": str(token), "access": str(token.access_token) }
        user_response = { "id":user.id, "username":user.username, "email":user.email, "first_name":user.first_name, "is_confirmed":user.is_confirmed, 'login':False,
                      "last_name":user.last_name, "image":user.photo.url, "inventory":user.inventory, "activation_email":email_msg, "referral":user.referral, "invitation_referral":user.invitation_referral }

        response = { 'token':token_response , 'user':user_response }
        return Response(response, status=status.HTTP_200_OK)













#-------------------------------------------------------- Profile -------------
class Profile(mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        banners = []
        for Banner in HomeBanners.objects.all():
            banner = {'title':Banner.title, 'image':Banner.img.url, 'link':Banner.link}
            banners.append(banner)

        profile = models.User.objects.get(id=self.request.user.id)

        daily_ceiling = WithdrawalCeiling.objects.get(id=1).daily
        monthly_ceiling = WithdrawalCeiling.objects.get(id=1).monthly
        daily_withdraw_ceiling_remains = daily_ceiling-sum(Transaction.objects.filter(source=str(request.user.username), type='withdrawal', status='success', created_at__gte=datetime.now()-timedelta(days=1)).values_list('amount', flat=True) )
        monthly_withdraw_ceiling_remains = monthly_ceiling-sum(Transaction.objects.filter(source=str(request.user.username), type='withdrawal', status='success', created_at__gte=datetime.now()-timedelta(days=30)).values_list('amount', flat=True) )

        data = {
                'id':profile.id, 'username':profile.username, 'first_name':profile.first_name,
                'last_name':profile.last_name, 'email':profile.email, 'is_confirmed':profile.is_confirmed, 'login':True, 'referral':profile.referral, "invitation_referral":profile.invitation_referral,
                'shop':profile.shop, 'photo':profile.photo.url, 'gender':profile.gender,
                'birthday':profile.birthday, 'country':profile.country.name, 'wallet_address':profile.wallet_address,
                'last_login':profile.last_login, 'inventory':profile.inventory, "daily_withdraw_ceiling_remains":daily_withdraw_ceiling_remains, "monthly_withdraw_ceiling_remains":monthly_withdraw_ceiling_remains,
                'banners':banners }
        return Response(data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        profile = models.User.objects.get(id=self.request.user.id)
        data=request.data
        data['email'] = profile.email
        data['username'] = profile.username

        if data['wallet_address']:
            addr = coinaddrvalidator.validate('eth', data['wallet_address'])
            if addr.valid:
                serializer = UserSerializer(profile, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                return Response('Wallet address is not valid',status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data['wallet_address']=''
            serializer = UserSerializer(profile, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


    def post(self, request, *args, **kwargs):
        try:
            file = request.data['file']
        except KeyError:
            return Response('Upload the file',status=status.HTTP_406_NOT_ACCEPTABLE)
        profile = models.User.objects.get(id=self.request.user.id)
        profile.photo = file
        profile.save()
        data = {"image":profile.photo.url}
        return Response(data, status=status.HTTP_200_OK)











#---------------------------------------------------------- Users -------------
class User(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            user = models.User.objects.get(username=self.kwargs["username"])
            serializer = UserSerializer(user)
        except:
            return Response('User not found', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)









#------------------------------------------------------ Activation -------------
class Activation(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        code = helper.random_code()
        profile = models.User.objects.get(id=self.request.user.id)
        profile.conf_code = code
        profile.save()
        if helper.send_code(profile, code):
            return Response("Activation code send to {}".format(profile.email) , status=status.HTTP_200_OK)
        else:
            return Response("Error sending email - Please try again!" , status=status.HTTP_400_BAD_REQUEST)





#------------------------------------------------------ Confirmation -----------
class Confirmation(APIView):
    serializer_class = ConfirmationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data = serializer.errors)

        profile = models.User.objects.get(id=self.request.user.id)
        if data['code'] == str(profile.conf_code):
            profile.is_confirmed = True
            profile.save()

            token = RefreshToken.for_user(profile)
            token_response = { "refresh": str(token), "access": str(token.access_token) }
            user_response = { "id":profile.id, "username":profile.username, "email":profile.email, 'is_confirmed':profile.is_confirmed, 'login':True, "first_name":profile.first_name,
                          "last_name":profile.last_name, "image":profile.photo.url, "inventory":profile.inventory, "referral":profile.referral, "invitation_referral":profile.invitation_referral }
            response = { 'token':token_response , 'user':user_response }

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response("User not verified", status=status.HTTP_406_NOT_ACCEPTABLE)













#------------------------------------------------------ Countries -------------
class Countries(APIView):
    serializer_class = CountriesSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        countries = models.Countries.objects.filter(available=True)
        serializer = CountriesSerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)











#---------------------------------------------------------- Users -------------

class Users(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = models.User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)














#------------------------------------------------------- Usernames ------------

class Usernames(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = models.User.objects.all().values_list('username', flat=True)
        return Response(users, status=status.HTTP_200_OK)












#------------------------------------------------------- ForgotPass ------------
class ForgotPass(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            code = helper.random_code()
            username = request.data['username']
            profile = models.User.objects.get(username=username)
            profile.conf_code = code
            profile.save()
            if helper.rest_pass_send_code(profile, code):
                return Response("Code send to {}".format(profile.email) , status=status.HTTP_200_OK)
            else:
                return Response("Error sending email - Please try again!" , status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("username not found, please try again" , status=status.HTTP_400_BAD_REQUEST)







#------------------------------------------------------- ForgotPass ------------
class ForgotPassConf(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        profile = models.User.objects.get(username=request.data['username'])
        code = request.data['code']
        newpass = request.data['newpass']

        if code == str(profile.conf_code):
            profile.set_password(newpass)
            profile.save()
            return Response("New password applied successfully" , status=status.HTTP_200_OK)
        else:
            return Response("The sent code does not match", status=status.HTTP_400_BAD_REQUEST)

















#------------------------------------------------------ notification -----------
class Notif(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        title = request.data['title']
        body = request.data['body']
        image = "url"
        user = request.data['user']
        try:
            device = FCMDevice.objects.filter(user=user)
            device.send_message(Message( notification=Notification(title=title, body=body, image=image ), data={ "username": "mohamad7" } ))
            return Response("notification sent successfully" , status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Error in sending notification", status=status.HTTP_400_BAD_REQUEST)







#--------------------------------------------------------- DataNotif -----------
class DataNotif(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            now = datetime.now()
            user = models.User.objects.get(id=request.data['user'])
            device = FCMDevice.objects.filter(user=request.data['user'])
            device.send_message(Message( data={ "username":user.username, "title":request.data['title'], "body":request.data['body'], "type":request.data['type'], "time":str(now) } ))
            notif = NotifLists()
            notif.title = request.data['title']
            notif.body = request.data['body']
            notif.type = request.data['type']
            notif.time = now
            notif.user = user
            notif.save()
            return Response("data notification sent successfully" , status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response("Error in sending data notification", status=status.HTTP_400_BAD_REQUEST)










#----------------------------------------------------- Transaction -------------
class NotifList(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotifListsSerializer
    queryset = NotifLists.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['time', 'type']
    search_fields = ['title', 'body']
    ordering_fields = ['time']

    def get(self, request, format=None):
        query = self.filter_queryset(NotifLists.objects.filter(user=self.request.user).order_by('-time')[:20])
        serializer = NotifListsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)















#--------------------------------------------------------- InvitedByMe -------------
class InvitedByMe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = models.User.objects.filter(referral=request.user.invitation_referral)
        print(users)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

















#End
