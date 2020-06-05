import socket
import threading
import multiprocessing
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(processName)-10s) (%(threadName)-10s) %(message)s'
)

def worker_thread(serversocket):
    while True:
        clientsocket, (client_address, client_port) = serversocket.accept()
        logging.debug(f"New client {client_address}:{client_port}")

        while True:
            try:
                data = clientsocket.recv(1024)
                logging.debug(f"Recv: {data} from {client_address}:{client_port}")
            except OSError:
                break

            if len(data) == 0:
                break

            sent_data = data
            while True:
                sent_len = clientsocket.send(data)
                if sent_len == len(data):
                    break
                sent_data = sent_data[sent_len:]
            logging.debug(f"Send: {data} to {client_address}:{client_port}")

        clientsocket.close()
        logging.debug(f"Bye-bye: {client_address}:{client_port}")

def worker_process(serversocket):
    NUMBER_OF_THREADS = 10
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker_thread,
            args=(serversocket,))
        thread.daemon = True
        thread.start()

    while True:
        time.sleep(1)

def main(host='localhost', port=9090):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    serversocket.bind((host, port))
    serversocket.listen(5)

    NUMBER_OF_PROCESS = multiprocessing.cpu_count()
    logging.debug(f"Number of processes {NUMBER_OF_PROCESS}")
    for _ in range(NUMBER_OF_PROCESS):
        process = multiprocessing.Process(target=worker_process,
            args=(serversocket,))
        process.daemon = True
        process.start()

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()