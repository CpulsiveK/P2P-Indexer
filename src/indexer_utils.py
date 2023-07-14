import json
import socket
import struct

SERVER_ADDR:str = socket.gethostbyname(socket.gethostname())
MULTICAST_ADDR:str = '<broadcast>'
MULTICAST_PORT:int = 10000
MESSAGE:str = SERVER_ADDR.encode()
TTL = struct.pack('b', 1)
PORT:int = 5050
BUFFER_SIZE:int = 1024


class RoutingInfoDataStructure:
    shared_files_info:dict = {}
    
    def createDataStructure(self, files:dict, id:str) -> None:
        if id in self.shared_files_info:
            for filesID in files:
                if filesID not in self.shared_files_info[id]:
                    self.shared_files_info[id][filesID] = files[filesID]
        else:
            self.shared_files_info[id] = files


def unicastIndexerAddr():
    unicastPort = 50000

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

     # Enable broadcasting on the socket
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the socket to the broadcast address and a specific port
    udp_socket.bind(('', unicastPort))

    print('Listening for new nodes')

    # Receive messages
    while True:
        data, address = udp_socket.recvfrom(BUFFER_SIZE)
        message = data.decode()
        print(f"Received message: {message} from {address}")

        if (message == "indexer ip?"):
            udp_socket.sendto(SERVER_ADDR.encode(), address)
            print(f"sent {SERVER_ADDR}")