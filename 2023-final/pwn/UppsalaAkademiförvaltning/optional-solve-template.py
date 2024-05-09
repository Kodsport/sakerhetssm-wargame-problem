from pwn import *
import time

exe = "./container/UppsalaAkademif\xc3\xb6rvaltning"
IP = "localhost"
PORT = 50000


DEBUG = False
LOCAL = True
WINDOWS = True


if WINDOWS:
    context.terminal = ["wt.exe", "-w", "0", "split-pane", "--", "wsl.exe", "-d", "Ubuntu", "--"]
else:
    context.terminal = ["terminator", "-e"] # or whatever terminal you use

context.timeout = 0.5

if LOCAL:
    if DEBUG:
        r = gdb.debug(exe)
    else:
        r = process(exe)
else:
    r = remote(IP, PORT)


def menu(handle=None, prompt=b":", option=None, inputs=(), output=lambda a: a):
    def decorate(fun):
        def wrap(*args, **kwargs):
            time.sleep(0.2)

            log.info(f"Performing {fun.__name__}")
            
            handle.sendline(str(option))
            out = handle.recvrepeat(0.1)
            
            if inputs != ():

                if len(inputs) != len(args):
                    log.warn(f"*Missing arguments to {fun.__name__}")

                for content, content_type in zip(args, inputs):
                    if content_type == int:
                        content = str(content)
                    
                    log.info(f"Sending {content}")
                    
                    if type(content) == str:
                        content = content.encode("iso-8859-1")
                    
                    handle.sendline(content)
        
            log.info(f"Done with {fun.__name__}")

            print("")

            try:
                out += r.recvrepeat(0.2)
            except:
                pass

            return output(out)
        return wrap
    return decorate

def table_parse(table):
    return [p for p in [[y.split(b": ")[1].strip() for y in x.split(b"\n") if b"|" in y and len(y.split(b": ")) == 2] for x in table.split(b"------------------------------\n") if x.strip()] if p]

@menu(handle=r, prompt=b"0. ", option=0)
def leave(out):
    return out

@menu(handle=r, prompt=b"0. ", option=1, inputs=(str, int))
def add_tenant(out):
    return out

@menu(handle=r, prompt=b"0. ", option=2, inputs=(str, int, int))
def add_apartment(out):
    return out

@menu(handle=r, prompt=b"0. ", option=3, inputs=(str,), output=lambda d: b"Removed" in d)
def remove_tenant(out):
    return out

@menu(handle=r, prompt=b"0. ", option=4, inputs=(str,), output=lambda d: b"Removed" in d)
def remove_apartment(out):
    return out

@menu(handle=r, prompt=b"0. ", option=5, output=table_parse)
def list_tenants(out):
    return out

@menu(handle=r, prompt=b"0. ", option=6, output=table_parse)
def list_apartments(out):
    return out

@menu(handle=r, prompt=b"0. ", option=7, inputs=(str, str))
def assign_apartment(out):
    return out

'''
Functions above can be used for all menu options in the program, you can leave them as is.
'''


def solve():
    pass


if __name__ == "__main__":
    solve()