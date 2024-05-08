# Run pulseview and dump channels 0-7 at 20kHz a few times to data.out
# 0-3 data
# 4: E

import csv

RAM = [None for _ in range(256)]

for f in "0.csv", "1.csv":
    r = csv.reader(open("datas/" + f))
    data = [list(map(int, line)) for line in list(r)[1:]]
    data = [{"D": line[:4][::-1], "e": line[5], "rs": line[7], "rw": line[6]} for line in data]

    last_data = None
    commands = []

    for lastRow, row in zip(data[:-1], data[1:]):
        # low edge
        if not row["e"] and lastRow["e"]:
            if last_data is not None:
                if last_data["rs"] != row["rs"] and last_data["rw"] != row["rw"]:
                    print("misaligned")
                    last_data = row
                else:
                    commands.append({"D": row["D"] + last_data["D"], "rw": row["rw"], "rs": row["rs"]})
                last_data = None
            else:
                last_data = row


    current_addr = None
    for row in commands:
        data = row["D"]
        if row["rs"] == 0 and row["rw"] == 0 and row["D"][7] == 1:
            addr = sum(b << i for i, b in enumerate(data[:7]))
            current_addr = addr
            print(f"SET DDRAM ADDR = {addr:02x}")
        elif row["rs"] == 1 and row["rw"] == 0:
            val = sum(b << i for i, b in enumerate(data[:7]))
            print(f"WRITE RAM      = {val:02x}")
            if current_addr is not None:
                RAM[current_addr] = val
        else:
            print(f'unknown RS = {row["rs"]}, RW = {row["rw"]}, D = {row["D"]}')

print("".join(chr(x) if x is not None else '?' for x in RAM))
