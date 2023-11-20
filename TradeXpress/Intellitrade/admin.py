from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Trader)
@admin.register(Trader)
class TraderAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email","is_active")
    search_fields = ["email", "first_name", "last_name"]
    ordering = ('email',)
    
admin.site.register(TraderSecret)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ("trade_user", "strike_symbol", "quantity", "entry_price", 
                    "entry_datetime", "exit_price", "exit_datetime", "is_active")
    search_fields = ["trade_user__email", "trade_user__first_name", "trade_user__last_name",
                     "strike_symbol"]
    list_filter = ("entry_datetime", "trade_user__email", "nifty_symbol", "is_active")
    ordering = ('-entry_datetime',)

@admin.register(TradeSignal)
class TradeSignalAdmin(admin.ModelAdmin):
    list_display = ("price", "signal_datetime", "nifty_symbol", "strike_symbol",
                    "transaction_type", "entry_price", "exit_price", "is_active", "sl_to_entry")
    search_fields = ["signal_datetime", "nifty_symbol__name", "strike_symbol", "entry_price", 
                     "transaction_type__type"]
    list_filter = ("signal_datetime", "is_active", "nifty_symbol")
    ordering = ('-signal_datetime',)

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ("type",)

@admin.register(NiftySymbol)
class NiftySymbolAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(StopLoss)
class StopLossAdmin(admin.ModelAdmin):
    list_display = ("nifty_symbol", "price")

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ("nifty_symbol", "price")

@admin.register(DayWiseStrike)
class DayWiseStrikeAdmin(admin.ModelAdmin):
    list_display = ("nifty_symbol", "week_day", "price")
    list_filter = ("nifty_symbol",)
    ordering = ('nifty_symbol', 'price')

admin.site.register(SystemConfig)
admin.site.register(TelegramConfig)
