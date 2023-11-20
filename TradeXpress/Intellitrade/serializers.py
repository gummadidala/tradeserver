from rest_framework import serializers
from .models import *

class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ('uuid', 'first_name', 'last_name', 'email')

class TraderSecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraderSecret
        fields = '__all__'

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'

class TradeSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeSignal
        fields = '__all__'

class TelegramConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramConfig
        fields = '__all__'

class NiftySymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiftySymbol
        fields = '__all__'

class StopLossSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopLoss
        fields = '__all__'

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'

class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = '__all__'