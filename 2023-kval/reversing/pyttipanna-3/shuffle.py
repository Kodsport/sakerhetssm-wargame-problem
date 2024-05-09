from secrets import init_seed, flag

assert init_seed < 800_000

SEED = init_seed
def randint(top):
    global SEED
    SEED = SEED * 0xE621 + 0xabcd

    return SEED % top

def shuffle(lst):
    out = [None for _ in range(len(lst))]

    for i in range(len(lst)):
        n_spots_left = len(lst) - i
        chosen_spot = randint(n_spots_left)

        count = 0
        for j in range(len(out)):
            if out[j] == None:
                if count == chosen_spot:
                    out[j] = lst[i]
                    break
                else:
                    count += 1

    return out

shuffled_flag = "".join(shuffle(list(flag)))
print(shuffled_flag)
