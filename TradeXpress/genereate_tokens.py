import time
import os
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'TradeXpress.settings'
application = get_wsgi_application()
from Intellitrade.models import *
from angel_api import Angel


def generateTokens():
    active_traders  = Trader.objects.filter(is_active=True)
    if active_traders is not None and len(active_traders) > 0:
        for trader in active_traders:
            trader_secret = TraderSecret.objects.get(trade_user=trader)
            if trader_secret:
                print('Generating Tokens for: {}'.format(trader_secret.trade_user.email))
                angel = Angel(trader_secret.trade_user.email)
                angel.loginByPassword()
                angel.generateTokens()
                time.sleep(1)

if __name__ == '__main__':
    generateTokens()