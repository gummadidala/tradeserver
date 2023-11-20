import time
from angel_api import Angel
from telegram_read import Tele
import traceback
import os
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'TradeXpress.settings'
application = get_wsgi_application()
from Intellitrade.models import *

if __name__ == '__main__':
    try:
        while True:
            tele_config = TelegramConfig.objects.all()[0]
            sleep_secs = tele_config.tele_sleep_secs
            tele = Tele()
            signals = tele.signals
            print(signals)
            active_signals = TradeSignal.objects.filter(is_active=True)
            active_users  = Trader.objects.filter(is_active=True)
            if signals and len(signals) > 0 and not active_signals and len(active_signals)<=0 and len(active_users) > 0:
                signals[0].is_active = True
                signals[0].save()
                angel = Angel(active_users[0].email, signals[0])
                trade = angel.prepareTrade()
                if trade:
                    for user in active_users:
                        usr_angel = Angel(user.email, signals[0])
                        print('Placing order for: {}'.format(user.email))
                        usr_angel.placeOrder(trade)
            time.sleep(sleep_secs)
    except Exception as e:
        print(traceback.format_exc())
