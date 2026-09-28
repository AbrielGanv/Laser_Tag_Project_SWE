import socket
import threading

SOURCE_IP = "127.0.0.1"     # Your local interface ( I will use 192.168.1.2)
BROADCAST_IP = "127.0.0.255"  # for testing with the hardware, I will use 192.168.1.255
BROADCAST_PORT = 7500
RECEIVE_PORT = 7501
BUFFER_SIZE = 4096


def broadcast_equipment_code(equipment_code, broadcast_ip=BROADCAST_IP, port=BROADCAST_PORT, source_ip=SOURCE_IP):

    #broadcasts one equipment code over UDP
    #equipment code is the ID assigned to a player
    #broadcast IP is the network brodcasting address
    #port is the UDP port that we are sending to. 

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(str(equipment_code).encode("utf-8"), (broadcast_ip, port))
    finally:
        sock.close() 


class UDPReceiver:
    """Listens on 0.0.0.0:RECEIVE_PORT in a background thread."""

    def __init__(self, on_message, host="0.0.0.0", port=RECEIVE_PORT):
        self.on_message = on_message        # called as on_message(text, addr)
        self.host = host
        self.port = port
        self._stop = threading.Event()
        self._sock = None
        self._thread = None

    def start(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._sock.settimeout(0.5)          # so the loop can notice stop()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while not self._stop.is_set():
            try:
                data, addr = self._sock.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                continue
            except OSError:
                break                       # socket closed during shutdown
            self.on_message(data.decode("utf-8", errors="ignore").strip(), addr)

    def stop(self):
        self._stop.set()
        if self._sock:
            self._sock.close()
        if self._thread:
            self._thread.join(timeout=1)

if __name__ == "__main__":
    print(f"Broadcasting from {SOURCE_IP} to {BROADCAST_IP}:{BROADCAST_PORT}")
    broadcast_equipment_code("500", broadcast_ip=BROADCAST_IP, port=BROADCAST_PORT)