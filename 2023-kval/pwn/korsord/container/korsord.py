#!/usr/bin/python3
import string

def format_loader(words):
    return f"""
{words[13][0]}mport {words[15]}
{words[13][1]}mport {words[5]}
{words[13][2]}rom {words[9]} import *

context.{words[11]} = '{words[2]}'
buf = {words[7]}({words[3]}ellcr{words[10][0]}ft.{words[3]}(), {words[11]}='{words[2]}')

m = {words[5]}.{words[5]}(-1, {words[10][1]}en(buf), prot=7, offset=0)
{words[6][0]}.{words[4]}(buf)

{words[6][1]}ddr = {words[15]}.{words[0]}_p({words[15]}.addressof({words[15]}.{words[0]}.from_buffer(m)))
{words[6][2]}tr = {words[15]}.{words[8]}(addr, {words[15]}.c_void_p).{words[1]}

{words[15]}.c_long.{words[12]}(id({words[10][2]}ist) + {words[14]}).{words[1]} = ptr
"""

print("Welcome to Korsord, please help me fix my loader!")
print("As a reward, I'll execute the loader for you :)")
print("This is what my loader looks like at the moment:")
print("----------------------------------------------")
print(format_loader(['******', '*****', '*****', '**', '*****', '****', '***', '***', '****', '***', '***', '****', '************', '***', '**', '******']))
print("----------------------------------------------")

words = []

for i in [*range(1, 10), 14]:
    words.append(input(f"{i} Down: "))

for i in [3, 8, 10, 11, 12, 13]:
    words.append(input(f"{i} Across: "))

charset = string.ascii_letters + string.digits + "_"

for word in words:
    assert all(x in charset for x in word)

try:
	code = format_loader(words)
except:
	print("Uh oh, that does not look right. I think my computer broke")
	exit(0)

print("You're saying that my loader is supposed to be")
print("----------------------------------------------")
print(code)
print("----------------------------------------------")

exec(code)
