import socket
import time

BEACON_PORT = 5005
BEACON_MESSAGE = b"VIDEO_SERVER_BEACON"

def start_beacon():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("", 0))

    print("Starting UDP beacon...")
    while True:
        sock.sendto(BEACON_MESSAGE, ('<broadcast>', BEACON_PORT))
        time.sleep(5)  # Send beacon every 5 seconds

if __name__ == "__main__":
    start_beacon()
