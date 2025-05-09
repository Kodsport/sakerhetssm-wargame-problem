#!/bin/sh

unzip chall
pycdc chall.pyc

# ...
# webbrowser.open('https://spongebob.fandom.com/wiki/Hydro-dynamic_spatula')
# print(''.join((lambda .0: for c in .0:
#  chr(c))((83, 83, 77, 123, 72, 74, 52, 76, 80, 95, 83, 48, 75, 51, 53, 125))))
# else:
# ...

python3 -c 'print(bytes([83, 83, 77, 123, 72, 74, 52, 76, 80, 95, 83, 48, 75, 51, 53, 125]))'
# b'SSM{HJ4LP_S0K35}'
