import threading
import time

def loop():
    while True:
        time.sleep(1)

def main():
    for _ in range(10000):
        t = threading.Thread(target=loop)
        t.start()
        print(threading.active_count())

