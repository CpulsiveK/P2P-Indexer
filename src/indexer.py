import json
import threading
from indexer_utils import *
from concurrent.futures import ThreadPoolExecutor
from ast import literal_eval


class Indexer:
    data_structure = RoutingInfoDataStructure()
    lock = threading.Lock()

    active_connections: dict = {}


    def threadHandler(self, client_socket: socket.SocketType, client_address):
        requestTypes: dict = {
            "makeFilePublic": self.indexReceivedPublicFiles,
            "searchFile": self.returnSearchedResult,
        }

        try:
            # Read the client request and handle it
            data = client_socket.recv(BUFFER_SIZE).decode().strip()

            print(f'Received request: {data}')
        except socket.error as error:
            print(error)
        
        if data == "searchFile":
            requestTypes[data](client_socket)
        else:
            id, request_type = data.split()

            if request_type in requestTypes:
                requestTypes[request_type](client_socket, id)

        with self.lock:
            self.active_connections[id] = client_address


    def startIndexer(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((SERVER_ADDR, PORT))
            server_socket.listen()

            print(
                F'[INDEXER]: {SERVER_ADDR} is listening on [PORT]: {PORT} for incoming connections...')

            executor = ThreadPoolExecutor(max_workers=10)
            executor.submit(unicastIndexerAddr)

            while True:
                client_socket, client_address = server_socket.accept()
                executor.submit(self.threadHandler,
                                client_socket, client_address)
        except socket.error as error:
            print(error)


    def indexReceivedPublicFiles(self, client_socket: socket.SocketType, id):
        files_to_be_indexed: str = client_socket.recv(BUFFER_SIZE).decode()

        if files_to_be_indexed != None:
            client_socket.close()

            files: dict = literal_eval(files_to_be_indexed)

            self.data_structure.createDataStructure(files, id)

            print(self.data_structure.shared_files_info)


    def returnSearchedResult(self, client_socket: socket.SocketType):
        file_name: str = client_socket.recv(BUFFER_SIZE).decode()
        print(file_name)

        ids_of_files_found: list[str] = {}

        for ids in self.data_structure.shared_files_info:
            for file in self.data_structure.shared_files_info[ids]:
                match_letters = ''
                if len(file) >= 3 and len(file_name) >= 3:
                    match_letters = file[:3]
                if match_letters in file_name or file == file_name:
                    ids_of_files_found[ids] = self.data_structure.shared_files_info[ids][file]+':'+file

        available_client_addr: dict = {}

        if len(ids_of_files_found) != 0:
            for ids in ids_of_files_found:
                if ids in self.active_connections:
                    addr: list = self.active_connections[ids][0]
                    file_path: str = ids_of_files_found[ids]
                    available_client_addr[addr] = file_path

            if len(available_client_addr) != 0:
                json_data = json.dumps(available_client_addr)
                print(json_data)

                try:
                    client_socket.sendall(json_data.encode())
                    client_socket.close()
                except socket.error as error:
                    client_socket.close()
                    print(error)
