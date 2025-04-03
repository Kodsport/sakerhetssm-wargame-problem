#!/usr/bin/env python3

import re

def randint(state, top):
    state = state * 0xE621 + 0xabcd
    return state, state % top

def shuffle(seed, lst):
    out = [None for _ in range(len(lst))]

    for i in range(len(lst)):
        n_spots_left = len(lst) - i
        seed, chosen_spot = randint(seed, n_spots_left)

        count = 0
        for j in range(len(out)):
            if out[j] == None:
                if count == chosen_spot:
                    out[j] = lst[i]
                    break
                else:
                    count += 1

    return out

target =         '{Mt-5et3a5}Sr1n-!5y1e-uh-3fm3txS'
target_pattern = '{M........}S...................S'
cand_flag = 'SSM{' + 'A'*(len(target)-5) + '}'
for cand_seed in range(800_000):
    cand_shuffle = ''.join(shuffle(cand_seed, list(cand_flag)))
    if re.match(target_pattern, cand_shuffle):
        print(cand_seed, cand_shuffle)
        positions = list(range(len(target)))
        shuffled_positions = shuffle(cand_seed, positions)
        print(''.join(target[shuffled_positions.index(i)] for i in range(len(shuffled_positions))))

# SSM{n3xt-t1m3-u5e-f15her-yat35!}
