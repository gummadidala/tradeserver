from rest_framework import generics
from .models import *
from .serializers import *

class TraderListCreateView(generics.ListCreateAPIView):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer

class TraderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer

class TraderSecretListCreateView(generics.ListCreateAPIView):
    queryset = TraderSecret.objects.all()
    serializer_class = TraderSecretSerializer

class TraderSecretRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TraderSecret.objects.all()
    serializer_class = TraderSecretSerializer

class TradeListCreateView(generics.ListCreateAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

class TradeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

class TransactionTypeListCreateView(generics.ListCreateAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer

class TransactionTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer

class TradeSignalListCreateView(generics.ListCreateAPIView):
    queryset = TradeSignal.objects.all()
    serializer_class = TradeSignalSerializer

class TradeSignalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TradeSignal.objects.all()
    serializer_class = TradeSignalSerializer

class TelegramConfigListCreateView(generics.ListCreateAPIView):
    queryset = TelegramConfig.objects.all()
    serializer_class = TelegramConfigSerializer

class TelegramConfigRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TelegramConfig.objects.all()
    serializer_class = TelegramConfigSerializer

class NiftySymbolListCreateView(generics.ListCreateAPIView):
    queryset = NiftySymbol.objects.all()
    serializer_class = NiftySymbolSerializer

class NiftySymbolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NiftySymbol.objects.all()
    serializer_class = NiftySymbolSerializer

class StopLossListCreateView(generics.ListCreateAPIView):
    queryset = StopLoss.objects.all()
    serializer_class = StopLossSerializer

class StopLossRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StopLoss.objects.all()
    serializer_class = StopLossSerializer

class TargetListCreateView(generics.ListCreateAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

class TargetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

class SystemConfigListCreateView(generics.ListCreateAPIView):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer

class SystemConfigRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer