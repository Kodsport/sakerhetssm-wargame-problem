#!/usr/bin/env python3
import sys
print(sys.version)

# Viktigt med trademark för vårt system
system='PyKlock 2000™'
def klock():
    return f'Just nu är klockan {round(__import__("time").time(),1)} (Copyright {system})\n'

prompt = '''Vad vill du göra?
1. Kolla klockan
2. Uppdatera klockan
3. Stänga av klockan
>> '''
while choice:=input(prompt):
    if choice=='1':
        print(klock())
    elif choice=='2':
        klock.__code__=klock.__code__.replace(co_code=bytes.fromhex(input()))
    elif choice=='3':
        exit(f'{system} stänger ned...')
