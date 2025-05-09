from sys import argv
from python import Python
from collections import List

fn main():
    var args = argv()
    if len(args) != 2:
        print("supply argument")
        return
    var inp = args[1]
    var flag_enc = List(17,17,15,57,54,42,43,49,29,43,49,29,54,42,39,29,36,55,54,55,48,39,63)
    if len(inp) != len(flag_enc):
        print("Incorrect length")
        return
    print("Checking password 🔥",end="")
    for i in range(10):
        try:
            Python.import_module("time").sleep(1)
        except:
            print("Something went wrong")
            return
        print("🔥", end="")
    print("\nDone checking: ",end="")
    var py = Python()
    var valid = True
    for i in range(len(flag_enc)):
        var c1 = String("c1 = '") + inp[i] + "'"
        valid = py.eval(StringRef(c1._steal_ptr(), c1.__len__()))
        var c2 = String("c2 = chr(") + flag_enc[i] + " ^ 0x42)"
        valid = py.eval(StringRef(c2._steal_ptr(), c2.__len__()))
        valid = py.eval("if c1 != c2:print('Incorrect');exit()")
    print("Correct")
    return
    
    