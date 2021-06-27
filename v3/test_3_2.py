from test_3_0 import MyUpbit
import os
import json


secret_file = os.path.join('..', 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())
access_key = secrets['sh']['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = secrets['sh']['UPBIT_OPEN_API_SECRET_KEY']

myUpbit = MyUpbit(access_key, secret_key, 'KRW-BTC', order_krw=30000, interval='minute3')
while True:
    print()
    market = myUpbit.run()
