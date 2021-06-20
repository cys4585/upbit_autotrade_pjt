import os
import jwt
import uuid
import hashlib
import json
from urllib.parse import urlencode
import pyupbit
import requests
from pprint import pprint
secret_file = os.path.join('.', 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())
access_key = secrets['sh']['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = secrets['sh']['UPBIT_OPEN_API_SECRET_KEY']
server_url = 'https://api.upbit.com'
upbit = pyupbit.Upbit(access_key, secret_key)
balances = upbit.get_balances()
pprint(balances)

balance = upbit.get_balance('KRW-BTC')
print(balance)
# query = {
#     'market': 'KRW-BTC',
#     'state': 'done',
#     'page': 4,
# }
# query_string = urlencode(query)


# query_string = "{}".format(query_string).encode()


# m = hashlib.sha512()
# m.update(query_string)
# query_hash = m.hexdigest()

# payload = {
#     'access_key': access_key,
#     'nonce': str(uuid.uuid4()),
#     'query_hash': query_hash,
#     'query_hash_alg': 'SHA512',
# }

# jwt_token = jwt.encode(payload, secret_key)
# authorize_token = 'Bearer {}'.format(jwt_token)
# headers = {"Authorization": authorize_token}

# res = requests.get(server_url + "/v1/orders", params=query, headers=headers)

# print(res.json())
