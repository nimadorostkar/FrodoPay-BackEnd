from rest_framework import serializers
from .models import Top, Features, Description, Banners, MobileBanners, Footer











class TopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Top
        fields = ('slogan_text', 'buttonText_text')
