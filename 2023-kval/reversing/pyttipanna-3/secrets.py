init_seed = 0x5CADE
flag = "SSM{n3xt-t1m3-u5e-f15her-yat35!}"
assert len(flag) == 32, f"Expected 32 byte flag, got {len(flag)}"
assert flag.count("S") == 2
assert flag.count("M") == 1
assert flag.count("{") == 1
