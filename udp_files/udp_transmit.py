import socket
import time

SOURCE_IP = "127.0.0.1"     # Your local interface ( I will use 192.168.1.2)
PORT = 7501             #Note that the port tells you which application/service is being broadcasted to.
BROADCAST_IP = "127.0.0.255"  # for testing with the hardware, I will use 192.168.1.255

def broadcast_equipment_code(equipment_code, broadcast_ip = BROADCAST_IP, port = PORT, source_ip=SOURCE_IP):

    #broadcasts one equipment code over UDP
    #equipment code is the ID assigned to a player
    #broadcast IP is the network brodcasting address
    #port is the UDP port that we are sending to. 

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #tells OS that the socket is allowed to send broadcast packets
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    #converts a string to bytes
    message = str(equipment_code).encode("utf-8")

    bytes_sent = sock.sendto(message, (broadcast_ip, port))

    sock.close()

if __name__ == "__main__":
    print(f"Broadcasting from {SOURCE_IP} to {BROADCAST_IP}:{PORT}")

    broadcast_equipment_code(
        "500",
        broadcast_ip="127.0.0.255",
        port=7501
    )