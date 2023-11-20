from django.urls import path
from . import views

urlpatterns = [
    path('traders/', views.TraderListCreateView.as_view(), name='trader-list-create'),
    path('traders/<uuid:pk>/', views.TraderRetrieveUpdateDestroyView.as_view(), name='trader-retrieve-update-destroy'),
    path('tradersecrets/', views.TraderSecretListCreateView.as_view(), name='tradersecret-list-create'),
    path('tradersecrets/<uuid:pk>/', views.TraderSecretRetrieveUpdateDestroyView.as_view(), name='tradersecret-retrieve-update-destroy'),
    path('trades/', views.TradeListCreateView.as_view(), name='trade-list-create'),
    path('trades/<uuid:pk>/', views.TradeRetrieveUpdateDestroyView.as_view(), name='trade-retrieve-update-destroy'),
    path('transactiontypes/', views.TransactionTypeListCreateView.as_view(), name='transactiontype-list-create'),
    path('transactiontypes/<int:pk>/', views.TransactionTypeRetrieveUpdateDestroyView.as_view(), name='transactiontype-retrieve-update-destroy'),
    path('tradesignals/', views.TradeSignalListCreateView.as_view(), name='tradesignal-list-create'),
    path('tradesignals/<uuid:pk>/', views.TradeSignalRetrieveUpdateDestroyView.as_view(), name='tradesignal-retrieve-update-destroy'),
    path('telegramconfigs/', views.TelegramConfigListCreateView.as_view(), name='telegramconfig-list-create'),
    path('telegramconfigs/<uuid:pk>/', views.TelegramConfigRetrieveUpdateDestroyView.as_view(), name='telegramconfig-retrieve-update-destroy'),
    path('niftysymbols/', views.NiftySymbolListCreateView.as_view(), name='niftysymbol-list-create'),
    path('niftysymbols/<uuid:pk>/', views.NiftySymbolRetrieveUpdateDestroyView.as_view(), name='niftysymbol-retrieve-update-destroy'),
    path('stoplosses/', views.StopLossListCreateView.as_view(), name='stoploss-list-create'),
    path('stoplosses/<uuid:pk>/', views.StopLossRetrieveUpdateDestroyView.as_view(), name='stoploss-retrieve-update-destroy'),
    path('targets/', views.TargetListCreateView.as_view(), name='target-list-create'),
    path('targets/<uuid:pk>/', views.TargetRetrieveUpdateDestroyView.as_view(), name='target-retrieve-update-destroy'),
    path('systemconfigs/', views.SystemConfigListCreateView.as_view(), name='systemconfig-list-create'),
    path('systemconfigs/<uuid:pk>/', views.SystemConfigRetrieveUpdateDestroyView.as_view(), name='systemconfig-retrieve-update-destroy'),
]
