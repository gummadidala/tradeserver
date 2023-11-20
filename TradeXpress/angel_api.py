import http.client
import json
import pyotp
import pyotp
from datetime import datetime
import datetime
import requests
import os
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'TradeXpress.settings'
application = get_wsgi_application()
from Intellitrade.models import *

class Angel:
    
    def __init__(self, user=None, trade_signal=None):
        self.user_config = TraderSecret.objects.get(trade_user__email=user)
        if trade_signal:
            self.trade_signal = trade_signal
            self.nifty_symbol = trade_signal.nifty_symbol.name
            self.transaction = trade_signal.transaction_type.type
            self.price = trade_signal.price
        # print("In Angel: {}".format(msg))
        self.user = user
        self.client_id = self.user_config.angel_client_id
        self.client_pin = self.user_config.angel_client_pin
        self.api_key = self.user_config.angel_api_key
        self.totp = pyotp.TOTP(self.user_config.angel_qr_code_token).now()
        self.conn = http.client.HTTPSConnection("apiconnect.angelbroking.com")

    def loginByPassword(self):
        payload = {
                    "clientcode": self.client_id,
                    "password": self.client_pin,
                    "totp": self.totp
                    # "totp": "498546"
                  }
        headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-UserType': 'USER',
                    'X-SourceID': 'WEB',
                    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
                    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
                    'X-MACAddress': 'MAC_ADDRESS',
                    'X-PrivateKey': self.api_key
                  }
        self.conn.request("POST", 
                          "/rest/auth/angelbroking/user/v1/loginByPassword",
                          json.dumps(payload),
                          headers)
        res = self.conn.getresponse()
        data = json.loads(res.read())
        print(data)
        if data.get('status'):
            data = data.get('data')
            self.user_config.jwtToken = data.get('jwtToken')
            self.user_config.refreshToken = data.get('refreshToken')
            self.user_config.feedToken = data.get('feedToken')
            self.user_config.save()

    def generateTokens(self):
        payload = {"refreshToken": self.user_config.refreshToken}
        headers = {
            'Authorization': 'Bearer {}'.format(self.user_config.jwtToken),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
            'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
            'X-MACAddress': 'MAC_ADDRESS',
            'X-PrivateKey': self.api_key
          }
        self.conn.request("POST",
                          "/rest/auth/angelbroking/jwt/v1/generateTokens",
                          json.dumps(payload),
                          headers)
        res = self.conn.getresponse()
        data = json.loads(res.read())
        print(data)
        if data.get('status'):
            data = data.get('data')
            self.user_config.jwtToken = data.get('jwtToken')
            self.user_config.refreshToken = data.get('refreshToken')
            self.user_config.feedToken = data.get('feedToken')
            self.user_config.save()
    
    def getNearestThursday(self):
        today = datetime.date.today()
        days_until_thursday = (3 - today.weekday()) % 7
        nearest_thursday = today + datetime.timedelta(days=days_until_thursday)
        formatted_date = nearest_thursday.strftime("%d%b%y")
        return formatted_date.upper()
    
    def getNearestWednesday(self):
        today = datetime.date.today()
        days_until_thursday = (2 - today.weekday()) % 7
        nearest_thursday = today + datetime.timedelta(days=days_until_thursday)
        formatted_date = nearest_thursday.strftime("%d%b%y")
        return formatted_date.upper()

    def getNearestTuesday(self):
        today = datetime.date.today()
        days_until_thursday = (1 - today.weekday()) % 7
        nearest_thursday = today + datetime.timedelta(days=days_until_thursday)
        formatted_date = nearest_thursday.strftime("%d%b%y")
        return formatted_date.upper()
    
    def getNearestClosingDay(self):
        if self.nifty_symbol in ["BANKNIFTY"]:
            return self.getNearestWednesday()
        elif self.nifty_symbol in ["NIFTY"]:
            return self.getNearestThursday()
        elif self.nifty_symbol in ["FINNIFTY"]:
            return self.getNearestTuesday()
        else:
            print("symbol not supported:{}".format(self.nifty_symbol))
        
    def getDayWisePrice1(self, price):
        today = datetime.date.today()
        weekday_number = today.weekday()
        # (Monday is 0 and Sunday is 6)
        if self.transaction == "BUY":
            if weekday_number in [0, 1]:
                price -= 300
            elif weekday_number in [2, 3]:
                price -= 200
            else:
                price -= 400
        else:
            if weekday_number in [0, 1]:
                price += 300
            elif weekday_number in [2, 3]:
                price += 200
            else:
                price += 400
        return price
    
    def getDayWisePrice(self, price):
        week_day = datetime.datetime.now().strftime('%A')
        day_strike_price_obj = DayWiseStrike.objects.get(week_day=week_day, nifty_symbol__name = self.nifty_symbol)
        day_strike_price = day_strike_price_obj.price if day_strike_price_obj is not None else 0
    
        if self.transaction == "BUY":
            price -= day_strike_price
        else:
            price += day_strike_price
        return int(price)

    def getTradeSymbol(self):
        extra_price = self.price % 100
        if self.transaction == "BUY":
            price= self.price - extra_price
            ce_pe = 'CE'
        else:
            price = self.price + (100-extra_price)
            ce_pe = 'PE'
        price = self.getDayWisePrice(price)
        trade_symbol = self.nifty_symbol + self.getNearestClosingDay() + str(price) + ce_pe
        return trade_symbol

    def getSymbolTokenAndLotsize(self, trade_symbol):
        api_endpoint = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        res = requests.get(api_endpoint)
        for obj in res.json():
          if obj.get("symbol") == trade_symbol:
              target_object = obj
              break
          else:
              target_object = None
        if target_object:
           return target_object

    def getLtp(self, symbol_token):
        payload = {
                      "mode": "FULL",
                      "exchangeTokens": {
                          "NFO": [symbol_token]
                      }
                  }
        headers = {
                    'X-PrivateKey': self.api_key,
                    'Accept': 'application/json',
                    'X-SourceID': 'WEB',
                    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
                    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
                    'X-MACAddress': 'MAC_ADDRESS',
                    'X-UserType': 'USER',
                    'Authorization': 'Bearer {}'.format(self.user_config.jwtToken),
                    'Accept': 'application/json',
                    'X-SourceID': 'WEB',
                    'Content-Type': 'application/json'
                  }
        self.conn.request("POST", "/rest/secure/angelbroking/market/v1/quote/", json.dumps(payload), headers)
        res = self.conn.getresponse()
        data = json.loads(res.read())
        if data.get('status'):
          data = data.get('data').get('fetched')[0]
          print("LTP: {}".format(data.get('ltp')))
          return data.get('ltp')

    def prepareTrade(self):
        try:
            trade_symbol = self.getTradeSymbol()
            print(trade_symbol)
            symbol_token_lotsize = self.getSymbolTokenAndLotsize(trade_symbol)
            # print(symbol_token_lotsize)
            ltp = self.getLtp(symbol_token_lotsize.get('token'))
            trade = {
                    'tradingsymbol': trade_symbol,
                    'symboltoken': symbol_token_lotsize.get('token'),
                    'lotsize': symbol_token_lotsize.get('lotsize'),
                    'ltp': str(ltp)
                    }
            print(trade)
            self.trade_signal.strike_symbol = trade_symbol
            self.trade_signal.symbol_token = symbol_token_lotsize.get('token')
            self.trade_signal.entry_price = ltp
            self.trade_signal.save()
            return trade
        except Exception as e:
            print("Error {}".format(e))
            self.trade_signal.is_active = False
            self.trade_signal.save()
            return None

    def placeOrder(self, trade):
        payload = {
                    "variety":"NORMAL",
                    "tradingsymbol":trade.get('tradingsymbol'),
                    "symboltoken":trade.get('symboltoken'),
                    "transactiontype":"BUY",
                    "exchange":"NFO",
                    "ordertype":"LIMIT",
                    "producttype":"CARRYFORWARD",
                    "duration":"DAY",
                    "price":trade.get('ltp'),
                    "squareoff":"0",
                    "stoploss":"0",
                    "quantity":trade.get('lotsize')
                  }
        headers = {
                    'Authorization': 'Bearer {}'.format(self.user_config.jwtToken),
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-UserType': 'USER',
                    'X-SourceID': 'WEB',
                    'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
                    'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
                    'X-MACAddress': 'MAC_ADDRESS',
                    'X-PrivateKey': self.api_key
                  }
        self.conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder", 
                      json.dumps(payload), 
                      headers)
        res = self.conn.getresponse()
        data = json.loads(res.read())
        print(data)
        if data.get('status'):
            data = data.get('data')
            trade_obj = Trade()
            trade_obj.trade_user = Trader.objects.get(email=self.user)
            trade_obj.strike_symbol = trade.get('tradingsymbol')
            trade_obj.nifty_symbol = NiftySymbol.objects.get(name=self.nifty_symbol)
            trade_obj.quantity = trade.get('lotsize')
            trade_obj.entry_price = trade.get('ltp')
            trade_obj.entry_order_id = data.get('orderid')
            trade_obj.entry_datetime = datetime.datetime.now()
            trade_obj.transaction_type = TransactionType.objects.get(type="BUY")
            trade_obj.trade_signal = self.trade_signal
            trade_obj.save()

    def exitOrder(self, ltp):
        print("Exit Order for: {} at {}".format(self.user, ltp))
        trade_obj = Trade.objects.get(trade_user__email = self.user, trade_signal=self.trade_signal, is_active=True)
        payload = {
                    "variety":"NORMAL",
                    "tradingsymbol":trade_obj.strike_symbol,
                    "symboltoken":self.trade_signal.symbol_token,
                    "transactiontype":"SELL",
                    "exchange":"NFO",
                    "ordertype":"MARKET",
                    "producttype":"CARRYFORWARD",
                    "duration":"DAY",
                    "price":ltp,
                    "squareoff":"0",
                    "stoploss":"0",
                    "quantity":trade_obj.quantity
                  }
        headers = {
                        'X-PrivateKey': self.api_key,
                        'Accept': 'application/json',
                        'X-SourceID': 'WEB',
                        'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
                        'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
                        'X-MACAddress': 'MAC_ADDRESS',
                        'X-UserType': 'USER',
                        'Authorization': 'Bearer {}'.format(self.user_config.jwtToken),
                        'Accept': 'application/json',
                        'X-SourceID': 'WEB',
                        'Content-Type': 'application/json'
                    }
        self.conn.request("POST", "/rest/secure/angelbroking/order/v1/placeOrder",
                            json.dumps(payload), 
                            headers)
        res = self.conn.getresponse()
        data = json.loads(res.read())
        print(data)
        if data.get('status'):
            data = data.get('data')
            self.trade_signal.is_active = False
            self.trade_signal.save()
            trade_obj.exit_price = ltp
            trade_obj.exit_order_id = data.get('orderid')
            trade_obj.exit_datetime = datetime.datetime.now()
            trade_obj.is_active = False
            trade_obj.save()

if __name__ == '__main__':
    # config = utils.read_json("system")
    # msg = {'tradingsymbol': 'NIFTY21SEP2319700CE', 'symboltoken': '54643', 'lotsize': '50', 'ltp': 'None'}
    # angel = Angel("system", msg, msg.get('symbol'))
    # angel.prepareTrade()
    angel = Angel("gkrkoti3@gmail.com")
    angel.loginByPassword()