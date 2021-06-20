import os, json
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import pyupbit

import requests
from pprint import pprint
import time

secret_file = os.path.join('..', 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())
access_key = secrets['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = secrets['UPBIT_OPEN_API_SECRET_KEY']
server_url = 'https://api.upbit.com'

# payload = {'access_key': access_key}
# jwt_token = jwt.encode(payload, secret_key)
# authorization_token = 'Bearer {}'.format(jwt_token)
# headers = {'Authorization': authorization_token}
# res = requests.get(server_url + '/v1/accounts', headers=headers)
# pprint(res.json())

upbit = pyupbit.Upbit(access_key, secret_key)
# pprint(upbit.get_balances())

def trade(coin):
    # print('#'*30)
    # print('trade() 실행! ')

    df = pyupbit.get_ohlcv(coin, interval='minute1')
    # print(df)
    close = df['close']

    ma2, ma6, ma10, ma20, ma40, ma60, ma80 = 0, 0, 0, 0, 0, 0, 0
    for i in range(-1, -81, -1):
        if i >= -80: ma80 += close[i]
        if i >= -60: ma60 += close[i]
        if i >= -40: ma40 += close[i]
        if i >= -20: ma20 += close[i]
        if i >= -10: ma10 += close[i]
        if i >= -6: ma6 += close[i]
        if i >= -2: ma2 += close[i]

    ma2 /= 2
    ma6 /= 6
    ma10 /= 10
    ma20 /= 20
    ma40 /= 40
    ma60 /= 60
    ma80 /= 80

    krw = 10000
    current_price = pyupbit.get_current_price(coin)
    weight = 0
    if coin == 'KRW-BTC':
        weight = 30000
    elif coin == 'KRW-BTG':
        weight = 60
    elif coin == 'KRW-ETH':
        weight = 2000
    elif coin == 'KRW-XRP':
        weight = 1

    print('weight: {}'.format(weight))
    print('current price: {:,}'.format(current_price))
    print('ma2: {:,}'.format(ma2))
    print('ma6: {:,}'.format(ma6))
    print('ma10: {:,}'.format(ma10))
    print('ma20: {:,}'.format(ma20))
    print('ma40: {:,}'.format(ma40))
    print('ma60: {:,}'.format(ma60))
    print('ma80: {:,}'.format(ma80))

    if current_price is not None and current_price + weight < ma6 < ma10 < ma20 < ma40 < ma60 < ma80:
        print('###감지 : 살 상황!###')

        ordered = upbit.buy_market_order(coin, krw)
        if ordered.get('error') is None:
            print(ordered.get('created_at'))    
            print('buy!')
        else:
            print('error!: {}'.format(ordered.get('error')))

        print('2분 정지')
        time.sleep(120) 

    elif current_price is not None and current_price - weight > ma6 > ma10 > ma20 > ma40 > ma60 > ma80:
        print('###감지 : 팔 상황!###')

        ordered = upbit.sell_market_order(coin, (krw + 100) / current_price)
        if ordered.get('error') is None:
            print(ordered.get('created_at'))    
            print('sell!')
        else:
            print('error!: {}'.format(ordered.get('error')))

        print('2분 정지')
        time.sleep(120)

    # print('2초 정지')
    time.sleep(5)
    # print('trade() 종료! ')
    