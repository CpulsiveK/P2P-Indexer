import socket
import struct
import time

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


def broadcastIndexerAddr():
    try:
        multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)

        while True:
            multicast_socket.sendto(MESSAGE, (MULTICAST_ADDR, MULTICAST_PORT))
            print(f"[BROADCASTING] {MESSAGE}............")
            time.sleep(5)
    except socket.error as error:
        print(error)