import socket
import threading
import time


def client_handler(sock: socket.socket):
    _ = sock.recv(1024)
    time.sleep(0.3)
    sock.sendall(
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/html\r\n"
        b"Content-Length: 71\r\n\r\n"
        b"<html><head><title>Success</title></head><body>Index page</body></html>"
    )
    sock.close()


def main(host: str = 'localhost', port: int = 9090) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind((host, port))
    sock.listen(128)
    print(f"Starting Web Server at {host}:{port}")
    try:
        while True:
            client_sock, (client_addr, client_port) = sock.accept()
            client_thread = threading.Thread(
                target=client_handler,
                args=(client_sock,))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        sock.close()


if __name__ == "__main__":
    main()

