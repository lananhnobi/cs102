import socket
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s'
)


def client_handler(sock: socket.socket, address: str, port: int) -> None:
    while True:
        try:
            message = sock.recv(1024)
            logging.debug(f"Recv: {message} from {address}:{port}")
        except OSError:
            break

        if len(message) == 0:
            break

        sent_message = message
        while True:
            sent_len = sock.send(sent_message)
            if sent_len == len(sent_message):
                break
            sent_message = sent_message[sent_len:]
        logging.debug(f"Send: {message} to {address}:{port}")
    sock.close()
    logging.debug(f"Bye-bye: {address}:{port}")


def main(host: str = 'localhost', port: int = 9090) -> None:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serversocket.bind((host, port))
    serversocket.listen(128)
    socket.setdefaulttimeout(10)

    print(f"Starting TCP Echo Server at {host}:{port}")
    try:
        while True:
            clientsocket, (client_address, client_port) = serversocket.accept()
            logging.debug(f"New client: {client_address}:{client_port}")
            client_thread = threading.Thread(
                target=client_handler,
                args=(clientsocket, client_address, client_port))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down")
    finally:
        serversocket.close()


if __name__ == "__main__":
    main()