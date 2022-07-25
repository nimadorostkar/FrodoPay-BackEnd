from rest_framework import serializers
from .models import WinnersList









class WinnersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinnersList
        fields = ('user')
