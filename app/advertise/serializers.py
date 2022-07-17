from rest_framework import serializers
from .models import Advertise







class AdvertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertise
        fields = ('image' ,'link')
