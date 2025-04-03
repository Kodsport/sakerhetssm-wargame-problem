#!/usr/bin/env python3

import secrets
import random
import sys

FLAG = sys.argv[1]

FUNC_TPL = """
jsval_t f_%d(struct js *js, jsval_t *args, int nargs)
{
    unsigned char key[] = { %s }; // %s
    for(size_t i = 0; i < %d; i++) {
        for(size_t j = 0; j < %d; j++) {
            scripts[i][j] ^= key[j];
        }
    }
    return js_mknum(0);
}"""

c_functions = {}

function_numbers = list(range(len(FLAG)))
random.shuffle(function_numbers)
script_params = zip(function_numbers, FLAG.encode())

scripts = []
for f_id, c in script_params:
    scripts.append((f_id, f"chr({c}); f_{f_id}();"))
scripts.append((None, f"flag()"))

max_script_len = max(len(script) for f_id, script in scripts)
scripts_data = [
    (f_id, secrets.token_bytes(max_script_len), x.ljust(max_script_len, " ").encode())
    for f_id, x in scripts
]

for data_idx, (enc_f_id, cur_key, _) in enumerate(scripts_data):
    for data_offset in range(data_idx + 1, len(scripts_data)):
        f_id, key, data = scripts_data[data_offset]
        scripts_data[data_offset] = (
            f_id,
            key,
            bytes(x ^ y for x, y in zip(data, cur_key)),
        )

with open("scripts.h", "w") as fout_h:
    hdr_top = """
    #include "elk.h"
    typedef struct {
        jsval_t (*func)(struct js *, jsval_t *, int);
        char* name;
    } funcdata;
    extern funcdata functable[%d];
    extern int result_idx;
    extern char result[%d];
    """ % (
        len(scripts_data) - 1,
        len(scripts_data),
    )
    fout_h.write(hdr_top + "\n")
    fout_h.write(
        f"extern unsigned char scripts[{len(scripts_data)}][{max_script_len+1}];\n"
    )

    with open("scripts.c", "w") as fout_c:
        scripts_array = [
            (idx, "{" + ", ".join(f"{x:#04x}" for x in data) + ", 0x00 }")
            for idx, (_, _, data) in enumerate(scripts_data)
        ]
        random.shuffle(scripts_array)
        answer = [x for x, _ in scripts_array]
        answer = [answer.index(x) for x in range(len(answer))]
        print(",".join(f"{x}" for x in answer))
        scripts_array_str = ", \n".join(y for _, y in scripts_array)
        fout_c.write('#include "scripts.h"\n')
        fout_c.write("int result_idx = 0;\n")
        fout_c.write("char result[%d] = { 0 };\n" % len(scripts_data))
        fout_c.write(
            f"unsigned char scripts[{len(scripts_data)}][{max_script_len+1}] = " + "{\n"
        )
        fout_c.write(scripts_array_str)
        fout_c.write("};\n")

        for idx in range(0, len(scripts_data) - 1):
            f_id, key, _ = scripts_data[idx]

            keystr = ", ".join(f"{x:#04x}" for x in key)
            func = FUNC_TPL % (
                f_id,
                keystr,
                key.hex(),
                len(scripts_data),
                max_script_len,
            )
            fout_c.write(func + "\n")
            fout_h.write(
                f"jsval_t f_{f_id}(struct js *js, jsval_t *args, int nargs);\n"
            )

        fout_c.write("funcdata functable[%d] = {\n" % (len(scripts_data) - 1))
        for f_id, _, _ in scripts_data[:-1]:
            fout_c.write('{.func = f_%d, .name = "f_%d" },\n' % (f_id, f_id))
        fout_c.write("};\n")
