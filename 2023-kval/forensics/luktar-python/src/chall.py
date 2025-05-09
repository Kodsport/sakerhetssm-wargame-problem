import sys
import time
import webbrowser

def print_slowly(msg, delay=0.1, sep=' '):
    for i, word in enumerate(msg.split(sep)):
        if i > 0: print(sep, end='')
        print(word, end='')
        sys.stdout.flush()
        time.sleep((delay[i]) if type(delay) is tuple else delay)
    print()

print_slowly('En stinkande stank som stinker', (0.3, 0.5, 0.3, 0.3, 0.5))
print_slowly('Stinkande ... ansjovis', 1)
print_slowly('Vad?', 1)
print_slowly('AN-SJO-VIS', 0.5, '-')

antal_ba = 25

for i in range(antal_ba):
    print_slowly(r''' ___  ___
| _ )/   \
| _ \| - |
|___/|_|_|''', (0.01,) * 3 + (0.10,), '\n')

    if i == antal_ba - 2: time.sleep(1)

time.sleep(1)

# webbrowser.open('https://open.spotify.com/track/1PmXm1881bonBI1AlG5uaH')

print()

print_slowly('Vad var det Svampbob skulle köpa?', (0.2, 0.2, 0.2, 0.4, 0.3, 0.5))

if input() == ''.join(chr(c) for c in [69, 110, 32, 104, 121, 100, 114, 111, 100, 121, 110, 97, 109, 105, 115, 107, 32, 115, 116, 101, 107, 115, 112, 97, 100, 101, 32, 109, 101, 100, 32, 115, 116, 121, 114, 45, 32, 111, 99, 104, 32, 98, 97, 98, 111, 100, 115, 116, 105, 108, 108, 115, 97, 116, 115, 101, 114, 32, 111, 99, 104, 32, 116, 117, 114, 98, 111, 100, 114, 105, 102, 116]):
    webbrowser.open('https://spongebob.fandom.com/wiki/Hydro-dynamic_spatula')
    print(''.join(chr(c) for c in [83, 83, 77, 123, 72, 74, 52, 76, 80, 95, 83, 48, 75, 51, 53, 125]))

else:
    print_slowly('Det kanske han skulle, det vet jag inte. Kolla här:', (0.2, 0.3, 0.2, 0.4, 0.2, 0.2, 0.2, 0.5, 0.3, 1))
    print('https://www.youtube.com/watch?v=euDDOMl-Ayc')
    webbrowser.open('https://www.youtube.com/watch?v=euDDOMl-Ayc')
