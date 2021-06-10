import os, json
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import pyupbit

import requests
from pprint import pprint

secret_file = os.path.join('.', 'secrets.json')
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
pprint(upbit.get_balances())

df = pyupbit.get_ohlcv('KRW-BTG', interval='minute1')
print(df)
close = df['close']

ma5, ma10, ma20, ma30 = 0, 0, 0, 0
for i in range(-1, -31, -1):
    if i >= -30: ma30 += close[i]
    if i >= -20: ma20 += close[i]
    if i >= -10: ma10 += close[i]
    if i >= -5: ma5 += close[i]

ma5 /= 5
ma10 /= 10
ma20 /= 20
ma30 /= 30
print(ma5, ma10, ma20, ma30)

if ma5 < ma10 < ma20 < ma30:
    print('사야해!')
elif ma5 > ma10 > ma20 > ma30:
    print('팔아야해!')
else:
    print('관망!')