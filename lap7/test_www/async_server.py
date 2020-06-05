import asyncore
import asynchat
import socket
import multiprocessing
import logging
import mimetypes
import os
import urllib
import argparse
from time import strftime, gmtime

from pprint import pprint



def url_normalize(path):
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1 + 3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    return path


class FileProducer(object):

    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


class AsyncServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9000):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print(f"Incoming connection from {addr}")
        AsyncHTTPRequestHandler(sock)

    def serve_forever(self):
        asyncore.loop()


class AsyncHTTPRequestHandler(asynchat.async_chat):

    def __init__(self, sock):
        super().__init__(sock)
        self.sock = sock
        self.collected_data = []
        self.parse_header = False

        self.set_terminator(b"\r\n\r\n")

    def collect_incoming_data(self, data):
        self.collected_data.append(data)
        self.headers = {}
        self.parse_header = False

    def found_terminator(self):
        self.parse_request()

    def parse_request(self):
        if not self.parse_header:
            headers = self.parse_headers()
            self.parse_header = True

            pprint(headers)

            if headers is None:
                self.send_error(400, "Bad Request")

            self.headers = headers

            if headers["method"] == "POST":
                self.send_error(403)
            else:
                self.handle_request()
        else:
            self.set_terminator(None)
            self.handle_request()

    def parse_headers(self):
        headers = {}
        data = "".join(list(map(str, self.collected_data))).split("\\r\\n")

        try:
            headers["method"] = data[0].split()[0][2:]
            headers["uri"] = data[0].split()[1]
            headers["protocol"] = data[0].split()[2]

            for key, value in list(map(lambda x: x.split(':', maxsplit=1), data[1:])):
                headers[str(key)] = value

            return headers

        except:
            pass

    def handle_request(self):
        method_name = 'do_' + self.headers["method"]

        if not hasattr(self, method_name):
            self.send_error(405)
            self.handle_close()
            return

        handler = getattr(self, method_name)
        handler()

    def send_error(self, code, message=None):
        try:
            short_msg, long_msg = self.responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg

        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Connection", "close")
        self.send_header("Content-Length", "71\r\n")
        self.end_headers()

    def send_header(self, keyword, value):
        self.sock.sendall(f'{keyword}: {value}\r\n'.encode())

    def send_response(self, code, message=''):
        self.sock.sendall(f'{self.headers["protocol"]} {code} {message}\r\n'.encode())

    def end_headers(self):
        self.sock.sendall(b'<html><head><title>Success</title></head><body>Index page</body></html>')

    def do_GET(self):
        self.body = {}
        self.send_response(200, 'OK')
        self.send_header("Date", gmtime())
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", "71\r\n")
        self.end_headers()

    def translate_path(self, path):
        pass

    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
    }


def parse_args():
    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=9000)
    parser.add_argument("--log", dest="loglevel", default="info")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default=".")
    return parser.parse_args()


def run():
    server = AsyncServer(host=args.host, port=args.port)
    server.serve_forever()


if __name__ == "__main__":
    args = parse_args()

    logging.basicConfig(
        filename=args.logfile,
        level=getattr(logging, args.loglevel.upper()),
        format="%(name)s: %(process)d %(message)s")
    log = logging.getLogger(__name__)

    DOCUMENT_ROOT = args.document_root
    for _ in list(range(args.nworkers)):
        p = multiprocessing.Process(target=run())
        p.start()