from angel_api import Angel
import datetime
import time
import os
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'TradeXpress.settings'
application = get_wsgi_application()
from Intellitrade.models import *

def trail_sl(entry_price, ltp, sl, trade):
    if ltp >= entry_price +  sl or trade.sl_to_entry:
        if not trade.sl_to_entry:
            trade.sl_to_entry = True
            trade.save()
        sl = 0
    return sl

def exitOrder():
    try:
        active_trades = TradeSignal.objects.filter(is_active=True)
        active_users = Trader.objects.filter(is_active=True)
        if active_users is not None and len(active_users) > 0:
            angel = Angel(active_users[0].email)
            if active_trades is not None and len(active_trades)>0:
                for trade in active_trades:
                    symbol_token = trade.symbol_token
                    ltp = angel.getLtp(symbol_token)
                    entry_price = trade.entry_price
                    sl = StopLoss.objects.get(nifty_symbol=trade.nifty_symbol).price
                    target = Target.objects.get(nifty_symbol=trade.nifty_symbol).price
                    # trail sl to entry if ltp is greater than entry by sl 
                    sl = trail_sl(entry_price, ltp, sl, trade)
                    if ltp >= entry_price + target or ltp <= entry_price - sl:
                        trade.exit_price = ltp
                        trade.exit_datetime = datetime.datetime.now()
                        trade.save()
                        for user in active_users:
                            angel = Angel(user.email, trade)
                            angel.exitOrder(ltp)
    except Exception as e:
        pass

if __name__ == '__main__':
    while True:
        exitOrder()
        time.sleep(1)
