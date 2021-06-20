from test_2_0 import MyUpbit
import os
import json


secret_file = os.path.join('..', 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())
access_key = secrets['ys']['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = secrets['ys']['UPBIT_OPEN_API_SECRET_KEY']

myUpbit = MyUpbit(access_key, secret_key, 'KRW-BTC', order_krw=30000, interval='minute1')
while True:
    print()
    print('#'*25)
    market = myUpbit.check_market()
    myUpbit.buy_sell_coin(market)
