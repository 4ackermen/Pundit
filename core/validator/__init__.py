import re
import shlex
import socket

from os import (
    getcwd,
    mkdir,
    path,
)

class Validator:
    def __init__(self, submission, filename, user, subs, tmp):
        self.user = user
        self.tag = subs
        self.tmp = tmp
        self.submission = submission
        self.filename = filename

    def recv(self):
        len = int(self.conn.recv(8))
        return self.conn.recv(len)

    def replace(self, old, new, filename):
        buf = open(filename).read().replace(old, new)
        open(filename, 'w').write(buf)

    def check(self):
        self.vport = randrange(10000, 65530)
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
        sock.bind(("", self.vport))
        sock.listen(10)
        self.conn, _ = sock.accept()
        status = self.recv().decode()
        return status
