import os
import json
import time
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests
import pyupbit

from pprint import pprint

# 매수 : 하락장에서 반등할 것 같을 때
# 매도 : 상승장에서 하락할 것 같을 때
class MyUpbit:

    def __init__(self, access_key, secret_key, market, order_krw, interval):
        self.access_key = access_key
        self.secret_key = secret_key
        self.upbit = pyupbit.Upbit(self.access_key, self.secret_key)
        self.market = market
        self.interval = interval
        self.order_krw = order_krw
        self.last_execution_price = float(pyupbit.get_current_price(self.market))

        if self.interval == 'minute1':
            self.stop_sec = 60
            self.sell_weight = 1.009
        elif self.interval == 'minute3':
            self.stop_sec = 180
            self.sell_weight = 1.02
        elif self.interval == 'minute5':
            self.stop_sec = 300
            self.sell_weight = 1.03


    def compute_moving_average(self, *args):
        df = pyupbit.get_ohlcv(self.market, interval=self.interval)
        close = df['close']
        ma = {}
        for arg in args:
            ma[arg] = sum(close[-arg:]) / arg
        return ma


    def check_market(self):
        print('check_market() run')
        ma = self.compute_moving_average(5, 10, 20, 40, 60, 80)
        # 약세시장(하락)
        if ma[5] < ma[10] < ma[20] < ma[40] < ma[60]:
            return 'bear'
        # 강세시장(상승)
        elif ma[5] > ma[10] > ma[20] > ma[40] > ma[60]:
            return 'bull'
        # 횡보(박스)
        else:
            return 'box'
        

    def buy_sell_coin(self, market):
        current_price = float(pyupbit.get_current_price(self.market))
        print('최근체결가: {:,} / 현재가: {:,}'.format(self.last_execution_price, current_price))
        if market == 'box':
            print('box')
            print(f'{self.stop_sec}초 정지')
            time.sleep(self.stop_sec)
            return
        while True:
            print()
            print(f'{market} market : 감시!')
            ma = self.compute_moving_average(1, 12)
            print('ma1: {:,} / ma12: {:,}'.format(ma[1], ma[12]))
            if ma[1] > ma[12]: print('{:,} > {:,}'.format(ma[1], ma[12]))
            elif ma[1] < ma[12]: print('{:,} < {:,}'.format(ma[1], ma[12]))
            else: print('{:,} == {:,}'.format(ma[1], ma[12]))
            
            current_price = pyupbit.get_current_price(self.market)
            print('최근체결가: {:,} / 현재가: {:,}'.format(self.last_execution_price, current_price))

            if market == 'bear' and ma[1] >= ma[12] and self.last_execution_price > current_price:
                print('buy!')
                ordered = self.upbit.buy_market_order(self.market, self.order_krw)
                if ordered.get('error') is None:
                    time.sleep(3)
                    pprint(ordered)
                    order = self.upbit.get_order(ordered['uuid'])
                    self.last_execution_price = float(order['trades'][0]['price'])
                    print('체결가: {:,}'.format(self.last_execution_price))
                else:
                    print('매수 실패')
                    print(ordered)
                print(f'{self.stop_sec}초 정지')
                time.sleep(self.stop_sec)
                return 
            elif market == 'bull' and ma[1] <= ma[12] and self.last_execution_price < current_price:
                print('sell!')
                balance = self.upbit.get_balance(self.market)   # 코인 보유량
                sell_amount = self.order_krw * self.sell_weight / current_price # 판매 희망량
                if balance >= sell_amount: ordered = self.upbit.sell_market_order(self.market, sell_amount)
                else: ordered = self.upbit.sell_market_order(self.market, balance)

                if ordered.get('error') is None:
                    time.sleep(3)
                    pprint(ordered)
                    order = self.upbit.get_order(ordered['uuid'])
                    self.last_execution_price = float(order['trades'][0]['price'])
                    print('체결가: {:,}'.format(self.last_execution_price))
                else:
                    print('매도 실패')
                    print(ordered)
                print(f'{self.stop_sec}초 정지')
                time.sleep(self.stop_sec)
                return 
            print(f'{self.stop_sec // 6}초 정지')
            time.sleep(self.stop_sec // 6)

