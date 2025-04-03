from __future__ import annotations
from typing import Optional, Dict, Tuple, List
from abc import ABC, abstractmethod

import asyncio
import traceback

import os
import random
import string
import queue
import urllib.request

import http_parse

class Event(ABC):
    pass

class NewSubmit(Event):
    def __init__(self, chunked: bool):
        self.chunked = chunked

    def __repr__(self) -> str:
        return f"NewSubmit(chunked={self.chunked})"

class KVReceived(Event):
    def __init__(self, k: str, v: str):
        self.k = k
        self.v = v

    def __repr__(self) -> str:
        return f"KVReceived(k={self.k!r}, v={self.v!r})"

def make_id() -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

connection_queues: Dict[str, asyncio.Queue[Event]] = {}

class NotFoundException(Exception):
    pass

# data_queue.get() == None => end of data
async def handle_request(req: http_parse.HTTPRequest, transport: asyncio.WriteTransport, data_queue: asyncio.Queue[Optional[bytes]]):
    print("handling request for", req.method, req.target)
    try:
        if req.target is None:
            raise NotFoundException()

        if req.method == b"GET":
            if req.target.startswith(b"/static/"):
                if b"/." in req.target or b'./' in req.target:
                    raise NotFoundException()

                path = req.target.decode()[1:]
                if not os.path.isfile(path):
                    raise NotFoundException()
                with open(path, "rb") as f:
                    content = f.read()
                base, ext = os.path.splitext(path)
                content_type = {
                    ".html": "text/html; charset=UTF-8",
                    ".png": "image/png",
                }.get(ext, "text/plain")

                transport.write(b'HTTP/1.1 200 OK\r\n')
                transport.write(b'Content-Type: ' + content_type.encode() + b'\r\n')
                transport.write(b'Content-Length: ' + str(len(content)).encode() + b'\r\n')
                transport.write(b'\r\n')
                transport.write(content)
                transport.close()
                return
            elif req.target is None or req.target == b'/':
                await start_chunky(req, transport)
                return
            else:
                raise NotFoundException()

        elif req.method == b"POST":
            if req.target.startswith(b'/submit-'):
                form_id = req.target[8:].decode()
                print("submit to form ", form_id)

                await handle_submit(form_id, req, data_queue, transport)
    except NotFoundException:
        await send_404(None, transport)
    except asyncio.CancelledError:
        pass
    except:
        traceback.print_exc()

async def handle_submit(form_id: str, req: http_parse.HTTPRequest, data_queue: asyncio.Queue[Optional[bytes]], transport: asyncio.WriteTransport):
    async def post_ev(ev: Event):
        if form_id in connection_queues:
            q = connection_queues[form_id]
            await q.put(ev)
        else:
            print("no queue found")

    current_key: str = ''
    current_value: Optional[str] = None

    await post_ev(NewSubmit(req.headers.get(b'transfer-encoding') == b'chunked'))

    while True:
        data = await data_queue.get()
        if data is None:
            print("post end of data")
            if current_value is not None and current_value != '':
                await post_ev(KVReceived(urllib.request.unquote(current_key), current_value))

            transport.write(b'HTTP/1.1 200 OK\r\n')
            transport.write(b'Content-Length: 0\r\n')
            transport.write(b'\r\n')
            transport.write(b'\r\n')
            transport.close()
            break

        print("posted", data, "to submit")

        for ch in data.decode():
            if current_value is None:
                if ch == '=':
                    current_value = ''
                else:
                    current_key += ch
            else:
                if ch == '&':
                    await post_ev(KVReceived(urllib.request.unquote(current_key), current_value))

                    current_key = ''
                    current_value = None
                else:
                    current_value += ch

FLAG = "SSM{ch3ck_0ut_c0r4l_sh03s_coOk1e_cl1cker}"
CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_{}"

qs = [
    ("första", "När hölls första SSM?", [
        ("2012", "2012", False),
        ("2013", "2013", False),
        ("2014", "2014", False),
        ("2015", "2015", False),
        ("2016", "2016", True),
        ("2017", "2017", False),
        ("2018", "2018", False),
        ("2019", "2019", False),
        ("2020", "2020", False),
    ]),
    ("bästa", "När hölls bästa SSM?", [
        ("2012", "2012", False),
        ("2013", "2013", False),
        ("2014", "2014", False),
        ("2015", "2015", False),
        ("2016", "2016", True),
        ("2017", "2017", True),
        ("2018", "2018", True),
        ("2019", "2019", True),
        ("2020", "2020", True),
        ("2021", "2021", True),
        ("2022", "2022", True),
    ]),
    ("uni", "Bästa universitetet?", [
        ("kth", "KTH", False),
        ("lund", "Lund Universitet", False),
        ("ch", "Chalmers", True),
    ]),
    ("kuvert", "Vad var INTE i kuvertet 2021?", [
        ("chips", "Chipspåse", True),
        ("mateusz", "Luft från Mateusz rum", False),
        ("chip", "Ett chip", False),
    ]),
    ("flagga", "Vilken flagga kom från en chall i SSM 2019?", [
        ("f", "SSM{Th1s_is_4nother_way_0f_3nc0ding_a_str1ng}", True),
        ("a", "watevr{b64_15_4_6r347_3ncryp710n_m37h0d}", False),
        ("p", "SSM{1_w1ll_4lw4y5_l0v3_p41n7_5843}", False),
    ]),
    ("kodsport", "Hur skrivs föreningen Säkerhets-SM går under?", [
        ("streck", "Kod-Sport", False),
        ("camel", "KodSport Sverige", False),
        ("mellan", "Kodsport Sverige", True),
        ("corr", "Kod sport", False),
    ]),
]

for i, ch in enumerate(FLAG):
    assert ch in CHARS
    qs.append((f"ch-{i}", f"Vad är tecken #{i} i flaggan?", [
        (f"l-{ord(ach)}", ach, ach == ch)
        for ach in CHARS
    ]))

def chunk_init(form_id: str) -> bytes:
    return f'''\
<html>
    <style>

@keyframes fade-in {{
    0% {{ opacity: 0%; }}
    100% {{ opacity: 100%; }}
}}

select, label {{
    animation: 0.5s ease-out 0s 1 fade-in;
}}
    </style>
    <link rel="stylesheet" href="static/style.css">
    <body>
        <h1 id="titel"> SSM QUIZ </h1>
        <h2> Hur mycket SSM kan du? </h2>
        <p id="result"> </p>
        <iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
        <form id="quiz" action="/submit-{form_id}" target="dummyframe" method="post">
    '''.encode()

def render_question(qid: str, question: str, answers: List[Tuple[str, str, bool]]) -> bytes:
    return f'''<label for="{qid}"> {question} </label>'''.encode() \
        + f'''<select id="{qid}" name="{qid}" form="quiz">'''.encode() \
        + b'\n'.join(
            f'<option value="{aid}"> {answer} </option>'.encode()
            for aid, answer, _ in answers
        ) \
        + b'</select> <br />'

def chunk_end() -> bytes:
    return '''\
            <input type="submit"></input>
        </form>
    </body>
    '''.encode()

async def start_chunky(req: http_parse.HTTPRequest, transport: asyncio.WriteTransport):
    form_id = make_id()
    submit_queue: asyncio.Queue[Event] = asyncio.Queue()
    connection_queues[form_id] = submit_queue

    resp = b'''\
HTTP/1.1 200 OK\r\n\
Content-Type: text/html; charset=UTF-8\r\n\
Transfer-Encoding: chunked\r\n\
Connection: keep-alive\r\n\
\r\n'''
    transport.write(resp)

    await asyncio.sleep(0.1)

    async def write_data(data: bytes):
        print("writing", data[:20], '...')
        transport.write(hex(len(data))[2:].encode() + b'\r\n' + data + b'\r\n')
        # transport.drain()

    async def end():
        transport.write(b'0\r\n\r\n')
        transport.close()

    await write_data(chunk_init(form_id))

    await asyncio.sleep(2)

    for qid, q, ans in qs:
        await write_data(render_question(qid, q, ans))
        await asyncio.sleep(0.1)

    await write_data(chunk_end())

    await asyncio.sleep(1)
    async def send_n_correct(n: int):
        await write_data(f'<style> #result::after {{ content: "{n}/{len(qs)} rätt"; }} </style>\n'.encode())

    n_correct = 0
    uses_chunked = False

    while True:
        resp = await submit_queue.get()
        print("Got response", resp)
        if isinstance(resp, NewSubmit):
            n_correct = 0
            if not resp.chunked:
                await write_data(f'<!-- /submit was accessed without Transfer-Encoding: chunked. Please use Transfer-Encoding: chunked for better user experience --> '.encode())
            uses_chunked = resp.chunked
            await send_n_correct(n_correct)

            await asyncio.sleep(1)
        elif isinstance(resp, KVReceived):
            is_correct = False
            for qid, _q, ans in qs:
                if qid != resp.k:
                    continue
                for aid, _a, corr in ans:
                    if aid == resp.v and corr:
                        is_correct = True

            print(resp, is_correct)
            if is_correct:
                n_correct += 1
                await send_n_correct(n_correct)
                if not uses_chunked:
                    await asyncio.sleep(0.3)

async def send_404(path: Optional[str], transport: asyncio.WriteTransport):
    if path is not None:
        content = b"404 not found: " + path.encode()
    else:
        content = b"404 not found :("

    content_type = "text/plain; charset=UTF-8"
    transport.write(b'HTTP/1.1 404 Not Found\r\n')
    transport.write(b'Content-Type: ' + content_type.encode() + b'\r\n')
    transport.write(b'Content-Length: ' + str(len(content)).encode() + b'\r\n')
    transport.write(b'\r\n')
    transport.write(content)
    transport.close()

class HTTPHandler(asyncio.Protocol):
    def __init__(self):
        self.transport: Optional[asyncio.BaseTransport] = None
        self.parser = http_parse.HTTPParser()

        self.request_handler: Optional[asyncio.Task] = None
        self.data_queue: asyncio.Queue[Optional[bytes]] = asyncio.Queue()

    def connection_made(self, transport):
        print("New connection")
        self.transport = transport

    def connection_lost(self, exc):
        print("(connection lost", exc, ")")
        if self.request_handler is not None:
            self.request_handler.cancel()

    def data_received(self, data):
        print("got", len(data), "bytes:", data[:64])
        if not self.parser.feed(data):
            print("(too much data)")
            assert self.transport is not None
            self.transport.close()

        if self.parser.header_done():
            if self.request_handler is None:
                assert self.transport is not None and isinstance(self.transport, asyncio.WriteTransport)
                self.request_handler = asyncio.create_task(handle_request(self.parser.req, self.transport, self.data_queue))

            while True:
                try:
                    chunk = self.parser.req.body.get_nowait()
                except queue.Empty:
                    break
                self.data_queue.put_nowait(chunk)

            if self.parser.is_complete():
                self.data_queue.put_nowait(None)
                return

async def main():
    print("hello from main")

    loop = asyncio.get_event_loop()
    srv = await loop.create_server(HTTPHandler, "0.0.0.0", 50000)
    print("starting server")
    await srv.serve_forever()


    # async def handle(reader, writer):
    #     p = http_parse.HTTPParser()
    #     data = await reader.read(10000)
    #     p.feed(data)

    #     print(p.req.target)
    #     await start_chunky(p.req, writer)

    # serv = await asyncio.start_server(handle, '0.0.0.0', 50000)
    # await serv.serve_forever()

asyncio.run(main())
