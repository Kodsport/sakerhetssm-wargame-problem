import sys

MAX_SEED = 800_000

# Reimplement randint from source in more reusable format
class RNG:
    def __init__(self, seed):
        self.SEED = seed

    def randint(self, top):
        self.SEED = self.SEED * 0xE621 + 0xabcd

        return self.SEED % top


    def shuffle(self, lst):
        out = [None for _ in range(len(lst))]

        for i in range(len(lst)):
            n_spots_left = len(lst) - i
            chosen_spot = self.randint(n_spots_left)

            count = 0
            for j in range(len(out)):
                if out[j] == None:
                    if count == chosen_spot:
                        out[j] = lst[i]
                        break
                    else:
                        count += 1

        return out

shuffled = "{Mt-5et3a5}Sr1n-!5y1e-uh-3fm3txS"

first_s = shuffled.index("S")
second_s = shuffled.rindex("S")
m = shuffled.rindex("M")
brace = shuffled.rindex("{")



def find_seed(ind_seq):
    # Find generated sequenc
    seq = []
    for i in range(len(ind_seq)):
        n_before = len(list(x for x in ind_seq[:i] if x < ind_seq[i]))
        seq.append(ind_seq[i] - n_before)

    # brute force search
    for SEED in range(0, MAX_SEED):
        r = RNG(SEED)
        death = False
        for i, s in enumerate(seq):
            if r.randint(len(shuffled) - i) != s:
                death = True
                break
        if not death:
            print("Found seed", hex(SEED), file=sys.stderr)

            indices = RNG(SEED).shuffle(list(range(len(shuffled))))

            init = ""
            for i in range(len(indices)):
                init += shuffled[indices.index(i)]
            if init[-1] != "}":
                print("Invalid solution", file=sys.stderr)
            else:
                print(init)


find_seed([first_s, second_s, m, brace])
find_seed([second_s, first_s, m, brace])
