from __future__ import annotations
from typing import Tuple, Dict, Optional
from abc import ABC, abstractmethod
from queue import Queue

class HTTPRequest:
    def __init__(self):
        self.method: Optional[bytes] = None
        self.target: Optional[bytes] = None
        self.version: Optional[bytes] = None
        self.headers: Dict[bytes, bytes] = {}

        self.body: Queue = Queue()

class ParseState(ABC):
    def __init__(self, req: HTTPRequest):
        self.req = req

    @abstractmethod
    def feed_byte(self, byte: bytes) -> ParseState:
        pass

    def accepts(self) -> bool:
        return True

class HeaderState(ParseState):
    pass

class InitState(HeaderState):
    def feed_byte(self, byte: bytes) -> ParseState:
        return ParseMethodState(self.req).feed_byte(byte)

class ParseMethodState(HeaderState):
    def __init__(self, req: HTTPRequest):
        super().__init__(req)
        self.method = b""

    def feed_byte(self, byte: bytes) -> ParseState:
        if byte == b' ':
            self.req.method = self.method
            return ParseTargetState(self.req)
        self.method += byte
        return self

class ParseTargetState(HeaderState):
    def __init__(self, req: HTTPRequest):
        super().__init__(req)
        self.target = b""

    def feed_byte(self, byte: bytes) -> ParseState:
        if byte == b' ':
            self.req.target = self.target
            return ParseVersionState(self.req)
        self.target += byte
        return self

class ParseVersionState(HeaderState):
    def __init__(self, req: HTTPRequest):
        super().__init__(req)
        self.version = b""
        self.expect_nl = False

    def feed_byte(self, byte: bytes) -> ParseState:
        if byte == b'\r':
            self.req.version = self.version
            self.expect_nl = True
        elif byte == b'\n' and self.expect_nl:
            return ParseHeaderNameState(self.req)
        else:
            self.version += byte
        return self

class ParseHeaderNameState(HeaderState):
    def __init__(self, req: HTTPRequest):
        super().__init__(req)
        self.name = b""

        self.expect_nl = False

    def feed_byte(self, byte: bytes) -> ParseState:
        if byte == b'\r':
            self.expect_nl = True
        elif byte == b'\n' and self.expect_nl:
            if b'content-length' in self.req.headers:
                try:
                    content_length = int(self.req.headers[b'content-length'])
                except ValueError:
                    content_length = 0

                return ParseBodyState(self.req, content_length)
            elif self.req.headers.get(b'transfer-encoding') == b'chunked':
                return ChunkLenParser(self.req)

            return ParseBodyState(self.req, 0)
        elif byte == b':':
            return ParseHeaderValueState(self.req, self.name.lower())
        else:
            self.name += byte
        return self

class ParseHeaderValueState(HeaderState):
    def __init__(self, req: HTTPRequest, name: bytes):
        super().__init__(req)
        self.name = name

        self.value = b""
        self.expect_nl = False

    def feed_byte(self, byte: bytes) -> ParseState:
        if byte == b'\r':
            if len(self.value) > 0 and self.value[0:1] == b' ':
                self.value = self.value[1:]
            self.req.headers[self.name] = self.value
            self.expect_nl = True
        elif byte == b'\n' and self.expect_nl:
            return ParseHeaderNameState(self.req)
        else:
            self.value += byte
        return self

class ParseBodyState(ParseState):
    def __init__(self, req: HTTPRequest, content_length: int):
        super().__init__(req)
        self.body = b""
        self.chars_left = content_length

    def feed_byte(self, byte: bytes) -> ParseState:
        self.body += byte
        self.chars_left -= 1

        if self.chars_left == 0:
            self.req.body.put(self.body)

        return self

    def accepts(self) -> bool:
        return self.chars_left > 0

HEX = b'0123456789abcdef'

class ChunkLenParser(ParseState):
    def __init__(self, req: HTTPRequest):
        super().__init__(req)
        self.len = 0
        self.expect_nl = False

    def feed_byte(self, byte: bytes) -> ParseState:
        if self.expect_nl and byte == b'\n':
            if self.len == 0:
                return ParseBodyState(self.req, 0)
            return ChunkDataParser(self.req, self.len)
        byte = byte.lower()
        if byte in HEX:
            val = HEX.index(byte)
            self.len = 0x10 * self.len + val
        elif byte == b'\r':
            self.expect_nl = True
            return self
        else:
            print("Invalid hex byte:", byte)
        return self

class ChunkDataParser(ParseState):
    def __init__(self, req: HTTPRequest, data_len: int):
        super().__init__(req)
        self.len = data_len
        self.data = b''
        self.expect_nl = False

    def feed_byte(self, byte: bytes) -> ParseState:
        if self.expect_nl:
            if byte != b'\n':
                print("Expected \\n 2 after data")
            self.req.body.put(self.data)

            return ChunkLenParser(self.req)
        if len(self.data) == self.len:
            self.expect_nl = True
            if byte != b'\r':
                print("Expected \\r after data")
            return self
        else:
            self.data += byte
            return self

class HTTPParser:
    def __init__(self):
        self.req = HTTPRequest()
        self.state: ParseState = InitState(self.req)

    def feed(self, data: bytes) -> bool:
        for ch in data:
            if self.state.accepts():
                self.state = self.state.feed_byte(bytes([ch]))
            else:
                print("too much data sadge")
                return False
        return True

    def is_complete(self) -> bool:
        return not self.state.accepts()

    def header_done(self) -> bool:
        return not isinstance(self.state, HeaderState)

if __name__ == "__main__":
    p = HTTPParser()
    REQ = b'''\
POST / HTTP/1.1\r\n\
Host: 0.0.0.0:50000\r\n\
User-Agent: curl/7.79.1\r\n\
Accept: */*\r\n\
Transfer-Encoding: chunked\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
\r\n\
6\r\n\
hello!\r\n\
'''
    p.feed(REQ)

    print(p.req.method)
    print(p.req.target)
    print(p.req.version)
    print(p.req.headers)
    print(p.req.body.get())
