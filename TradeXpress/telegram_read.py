from telethon import TelegramClient, types
import time
# from utils import read_json, write_json
import traceback
import os
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'TradeXpress.settings'
application = get_wsgi_application()
from Intellitrade.models import *


class Tele:

    def __init__(self):
        self.config = TelegramConfig.objects.all()[0]
        self.api_id = self.config.tele_api_id
        self.api_hash = self.config.tele_api_hash
        self.last_message_id = self.config.tele_last_message_id
        self.tele_peer_channel_id = self.config.tele_peer_channel_id
        self.msg_limit = self.config.tele_msg_limit
        self.signals = []
        self.trade_symbols = [symbol.name for symbol in NiftySymbol.objects.all()]
        self.read_telegram()
    
    def read_telegram(self):
        try:
            with TelegramClient('kv_session', self.api_id, self.api_hash) as client:
                for message in client.iter_messages(types.PeerChannel(self.tele_peer_channel_id), limit=self.msg_limit):
                    if 'STGOPT' in message.message:
                        # print(message.id, message.date, message.message)
                        if message.id > self.last_message_id:
                            print(message.message)
                            self.config.tele_last_message_id = int(message.id)
                            self.config.save()
                            return self.parse_data(message.message)
        except Exception as e:
            print(str(e))
            pass

    def parse_data(self, msg):
        try:
            msg = msg.split('STGOPT')[1]
            msgs = msg.split(', ')
            action = "SELL" if 'sell' in msgs[0].lower() else "BUY"
            msgs = msgs[1:-1]
            for msg in msgs:
                msg = msg.split(' - ')
                if msg[0] == "NIFTYFINSERVICE":
                    msg[0] = "FINNIFTY"
                if msg[0] in self.trade_symbols:
                    trade_signal = TradeSignal()
                    trade_signal.price = int(float(msg[1]))
                    trade_signal.nifty_symbol = NiftySymbol.objects.get(name=msg[0])
                    trade_signal.transaction_type = TransactionType.objects.get(type=action)
                    trade_signal.save()
                    # json_res = {
                    #             "transaction": action,
                    #             "symbol": msg[0],
                    #             "price": int(float(msg[1]))
                    #         }
                    self.signals.append(trade_signal)
        except Exception as e:
            print(traceback.format_exc())

if __name__ == '__main__':
    tele = Tele()
    print(tele.signals)
