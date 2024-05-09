#!/usr/bin/env python3

import sys

flag = b"SSM{th3y_f1n411y_137_m3_1n}"

def handle(request):
    username, password = request.split(":")

    if username == "ADMIM" and password == "UL7R4S3CR37":
        sys.stdout.buffer.write(b"AUTHENTICATED")

    elif username == "AUTHENTICATED":
        if password == "ADMIN":
            sys.stdout.buffer.write(flag)
        elif password == "GUEST":
            sys.stdout.buffer.write(b"Why did you even check this? Anyway, here is a treat: https://www.youtube.com/watch?v=pROomL6IiOw")
        else:
            sys.stdout.buffer.write(b"\"%s\" NOT IN [\"ADMIN\",\"GUEST\"]" % password.encode())
    else:
        sys.stdout.buffer.write(b"UNAUTHENTICATED")

if __name__ == "__main__":
    try:
        handle(input(""))
    except:
        sys.stdout.buffer.write(b"UNAUTHENTICATED")
