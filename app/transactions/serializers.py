from rest_framework import serializers
from .models import Transaction, DepoHash





class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id' ,'source', 'destination', 'amount', 'normalize_amount', 'type', 'status', 'description', 'fee', 'normalize_fee', 'created_at')









class DepoHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepoHash
        fields = '__all__'
