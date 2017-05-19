
"""
    See https://cex.io/rest-api
"""
import hmac
import hashlib
import time
import requests

BASE_URL = 'https://cex.io/api/%s/'

class Api:
    """
    Python wrapper for CEX.IO
    """
    def __init__(self, username, api_key, api_secret):
        self.username = username
        self.api_key = api_key
        self.api_secret = api_secret

    @property
    def __nonce(self):
        return str(int(time.time() * 1000))

    @property
    def __signature(self):
        message = self.__nonce + self.username + self.api_key
        signature = hmac.new(bytearray(self.api_secret.encode('utf-8')), message.encode('utf-8'), digestmod = hashlib.sha256).hexdigest().upper()
        return signature

    def api_call(self, method, param=None, private=False, action=''):
        """
        :param method: Query method for getting info
        :type method: str

        :param param: Extra options for query
        :type options: dict

        :return: JSON response from CEX.IO
        :rtype : dict
        """
        if param is None:
            param = {}

        if private:
            param.update({
                'key': self.api_key,
                'signature': self.__signature,
                'nonce': self.__nonce
            })
        
        request_url = (BASE_URL % method) + action
        result = self.__post(request_url, param)

        return result

    def last_price(self, market='BTC/USD'):
        return self.api_call('last_price', None, False, market)

    def ticker(self, market='BTC/USD'):
        """
        :param market: String literal for the market (ex: BTC/ETH)
        :type market: str

        :return: Current values for given market in JSON
        :rtype : dict
        """
        return self.api_call('ticker', None, True, market)

    @property
    def balance(self):
        return self.api_call('balance', None, True)
    
    @property
    def get_myfee(self):
        return self.api_call('get_myfee', None, True)

    @property
    def currency_limits(self):
        return self.api_call('currency_limits', None, False)

    def convert(self, amount=1, market='BTC/USD'):
        """
        Converts any amount of the currency to any other currency by multiplying the amount 
        by the last price of the chosen pair according to the current exchange rate.

        :param amount: Convertible amount
        :type amount: float

        :return: Amount in the target currency
        :rtype: dict
        """
        return self.api_call('convert', { 'amnt': amount }, False, market)
    
    def open_orders(self, market):
        return self.api_call('open_orders', None, True, market)

    def cancel_order(self, order_id):
        return self.api_call('cancel_order', { 'id': order_id }, True)

    def buy_limit_order(self, amount, price, market):
        params =  {
            'type': 'buy',
            'amount': amount,
            'price': price
        }

        return self.api_call('place_order', params, True, market)

    def sell_limit_order(self, amount, price, market):
        params =  {
            'type': 'sell',
            'amount': amount,
            'price': price
        }

        return self.api_call('place_order', params, True, market)

    def open_long_position(self, amount, symbol, estimated_open_price, stop_loss_price, leverage=2, market='BTC/USD'):
        params = {
            'amount': amount,
            'symbol': symbol,
            'leverage': leverage,
            'ptype': 'long',
            'anySlippage': 'true',
            'eoprice': estimated_open_price,
            'stopLossPrice': stop_loss_price
        }

        return self.api_call('open_position', params, True, market)

    def open_short_position(self, amount, symbol, estimated_open_price, stop_loss_price, leverage=2, market='BTC/USD'):
        params = {
            'amount': amount,
            'symbol': symbol,
            'leverage': leverage,
            'ptype': 'short',
            'anySlippage': 'true',
            'eoprice': estimated_open_price,
            'stopLossPrice': stop_loss_price
        }

        return self.api_call('open_position', params, True, market)

    def open_positions(self, market='BTC/USD'):
        return self.api_call('open_positions', None, True, market)

    def close_position(self, position_id, market='BTC/USD'):
        return self.api_call('close_position', { 'id': position_id }, True, market)

    def get_order(self, order_id):
        return self.api_call('get_order', { 'id': order_id }, True)

    def order_book(self, depth=1, market='BTC/USD'):
        return self.api_call('order_book', None, False, market + '/?depth=' + str(depth))

    def trade_history(self, since=1, market='BTC/USD'):
        return self.api_call('trade_history', None, False, market + '/?since=' + str(since))

    def __post(self, url, param):
        result = requests.post(url, data=param, headers={ 'User-agent': 'bot-cex.io-' + self.username }).json()
        return result
