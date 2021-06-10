import os, json
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

secret_file = os.path.join('.', 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())
access_key = secrets['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = secrets['UPBIT_OPEN_API_SECRET_KEY']
server_url = 'https://api.upbit.com'

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = f'Bearer {jwt_token}'
headers = {'Autorization': authorize_token}

res = requests.get(server_url + '/v1/accounts', headers=headers)

print(res.json())