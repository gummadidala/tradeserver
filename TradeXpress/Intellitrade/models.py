from django.db import models
import uuid

class NiftySymbol(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class StopLoss(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    nifty_symbol = models.ForeignKey(NiftySymbol, on_delete=models.CASCADE)
    def __str__(self):
        return f"Stop Loss for {self.nifty_symbol}: {self.price}"

class Target(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    nifty_symbol = models.ForeignKey(NiftySymbol, on_delete=models.CASCADE)
    def __str__(self):
        return f"Target for {self.nifty_symbol}: {self.price}"

class Trader(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class TraderSecret(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trade_user = models.ForeignKey(Trader, on_delete=models.CASCADE)
    angel_client_id = models.CharField(max_length=255)
    angel_client_pin = models.CharField(max_length=255)
    angel_api_key = models.CharField(max_length=255)
    angel_qr_code_token = models.CharField(max_length=255)
    jwtToken = models.TextField(default=None, null=True, blank=True)
    refreshToken = models.TextField(default=None, null=True, blank=True)
    feedToken = models.TextField(default=None, null=True, blank=True)
    def __str__(self):
        return f"Secrets for Trader: {self.trade_user.first_name} {self.trade_user.last_name}"

class TransactionType(models.Model):
    TRANSACTION_CHOICES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    type = models.CharField(max_length=4, choices=TRANSACTION_CHOICES, unique=True)
    def __str__(self):
        return self.get_type_display()

class TradeSignal(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    signal_datetime = models.DateTimeField(auto_now_add=True)
    nifty_symbol = models.ForeignKey(NiftySymbol, on_delete=models.CASCADE)
    strike_symbol = models.CharField(max_length=255, null=True, blank=True)
    symbol_token = models.CharField(max_length=255, null=True, blank=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exit_datetime = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    sl_to_entry = models.BooleanField(default=False)
    def __str__(self):
        return f"TradeSignal - {self.transaction_type.get_type_display()} - {self.nifty_symbol} at Rs. {self.price} on {self.signal_datetime}"
    
class Trade(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trade_user = models.ForeignKey(Trader, on_delete=models.CASCADE)
    strike_symbol = models.CharField(max_length=255)
    nifty_symbol = models.ForeignKey(NiftySymbol, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    entry_datetime = models.DateTimeField(auto_now_add=True)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exit_datetime = models.DateTimeField(null=True, blank=True)
    entry_order_id = models.CharField(max_length=255)
    exit_order_id = models.CharField(max_length=255, null=True, blank=True)
    trade_date = models.DateField(auto_now_add=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    trade_signal = models.ForeignKey(TradeSignal, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"Trade for {self.trade_user}: {self.quantity} shares of {self.strike_symbol} at Rs. {self.entry_price} on {self.trade_date}"

class TelegramConfig(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tele_api_id = models.PositiveIntegerField()
    tele_api_hash = models.CharField(max_length=255)
    tele_sleep_secs = models.PositiveIntegerField(default=10)
    tele_peer_channel_id = models.BigIntegerField()
    tele_msg_limit = models.PositiveIntegerField(default=5)
    tele_last_message_id = models.PositiveIntegerField()
    def __str__(self):
        return "Telegram Configuration"

class SystemConfig(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exit_order_sleep_secs = models.PositiveIntegerField(default=0)
    def __str__(self):
        return "System Configuration"

class DayWiseStrike(models.Model):
    WEEK_DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    nifty_symbol = models.ForeignKey(NiftySymbol, on_delete=models.CASCADE)
    week_day = models.CharField(max_length=10, choices=WEEK_DAY_CHOICES)
    def __str__(self):
        return f"{self.nifty_symbol} - Rs.{self.price} - {self.get_week_day_display()}"
    class Meta:
        unique_together = ('nifty_symbol', 'week_day')



