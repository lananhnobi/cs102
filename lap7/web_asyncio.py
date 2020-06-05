import asyncio
from asyncio import StreamReader, StreamWriter


async def client_handler(reader: StreamReader, writer: StreamWriter) -> None:
    data: bytes = await reader.read(1024)
    await asyncio.sleep(0.3)
    writer.write(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/html\r\n"
        b"Content-Length: 71\r\n\r\n"
        b"<html><head><title>Success</title></head><body>Index page</body></html>"
    )
    await writer.drain()
    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(client_handler, '127.0.0.1', 9090, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
