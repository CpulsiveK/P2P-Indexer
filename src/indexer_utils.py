import socket
import struct

SERVER_ADDR:str = socket.gethostbyname(socket.gethostname())
MULTICAST_ADDR:str = '224.0.0.1'
MULTICAST_PORT:int = 10000
MESSAGE:str = SERVER_ADDR.encode()
TTL = struct.pack('b', 1)
PORT:int = 5050
BUFFER_SIZE:int = 1024


class RoutingInfoDataStructure:
    shared_files_info:dict = {}
    
    def createDataStructure(self, files:list[str], id:str) -> None:
        self.shared_files_info.setdefault(id, []).extend(files)
    

    def search(self, filename:str) -> list[str]:
        ids_of_files_found:list[str] = []

        for id in self.shared_files_info:
            for file in self.shared_files_info[id]:
                if file == filename:
                    ids_of_files_found.append(id)
        
        if len(ids_of_files_found) == 0:
            return None
        else:
            return ids_of_files_found


def unicastIndexerAddr():
    unicastPort = 10000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the socket options to allow broadcasting
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the socket to a specific address and port
    server_address = ('', unicastPort)
    sock.bind(server_address)

    print('Listening for new nodes')

    # Receive messages
    while True:
        data, address = sock.recvfrom(BUFFER_SIZE)
        message = data.decode()
        print(f"Received message: {message} from {address}")

        if (message == "indexer ip?"):
            sock.sendto(SERVER_ADDR.encode(), address)
            print(f"sent {SERVER_ADDR}")