#!/usr/bin/env python3

def main():
    p = 84110607885424435789520899428064591379192332213262905744967612163375651444019
    q = 67829743147343394076748419759397419634107631589392973908325370212997597011613
    d = 2213586969474081412462124297644928143705359494098619937248568620130781387315122350943336924430305120870587389920200952126423912501926700805309031037044579
    N = p*q

    print("Skicka ditt meddelande (ett heltal):")
    c = int(input())

    m = pow(c,d,N)

    msg = bytes.fromhex(hex(m)[2:])
    if msg==b"Hi Alice! This is a secret message.":
        with open("flag", "r") as fin:
            flag = fin.read()
        print("Hi Bob! Here is the flag:")
        print(flag)
    else:
        print("nope!")

if __name__ == "__main__":
    main()
