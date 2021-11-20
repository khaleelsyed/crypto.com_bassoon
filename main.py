import os
import hmac
import hashlib
import json
import requests
import websocket
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ['READONLY_KEY']
API_SECRET = os.environ['READONLY_SECRET']

req = {
	'id': 11,
	'method': 'private/get-order-detail',
	'api_key': API_KEY,
	'params': {'order_id': '337843775021233500'},
	'nonce': int(time.time() * 1000)
}

paramString = ""

# Ensure the parameters are alphabetically sorted by key
if 'params' in req:
	for key in sorted(req['params']):
		paramString += key
		paramString += str(req['params'][key])

sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])

req['sig'] = hmac.new(
		bytes(str(API_SECRET), 'utf-8'),
		msg=bytes(sigPayload, 'utf-8'),
		digestmod=hashlib.sha256
	).hexdigest()

# NOTE: Not tested
response = requests.get(req)
