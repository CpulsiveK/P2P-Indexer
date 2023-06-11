from indexer_utils import *
from concurrent.futures import ThreadPoolExecutor
from ast import literal_eval


class Indexer:
    data_structure = RoutingInfoDataStructure()

    def __init__(self):
        self.active_connections: dict = {}

    def threadHandler(self, client_socket: socket.SocketType, client_address):
        requestTypes: dict = {
            "makeFilePublic": self.indexReceivedPublicFiles,
            "searchFile": self.returnSearchedFiles
        }

        # Read the client request and handle it
        data = client_socket.recv(BUFFER_SIZE).decode().strip()
        print(f'Received request: {data}')

        id, request_type = data.split()

        if request_type in requestTypes:
            requestTypes[request_type](client_socket, id)

        self.active_connections.setdefault(id, '').extend(client_address[0])
        print(self.active_connections)

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

        if files_to_be_indexed:
            client_socket.close()

            files: dict = literal_eval(files_to_be_indexed)

            self.data_structure.createDataStructure(files, id)
            print(self.data_structure.shared_files_info)


    def returnSearchedFiles(self, client_socket: socket.SocketType, id):
        file_name: str = client_socket.recv(BUFFER_SIZE).decode()

        result: None or list(str) = self.data_structure.search(file_name)

        if result != None:
            available_client_addresses: list[tuple[str, str]] = []

            for id in result:
                if id in self.active_connections:
                    available_client_addresses.append(
                        id, self.active_connections[id])

            for address in available_client_addresses:
                for content in address:
                    client_socket.send(content.encode())

            print("File found")
        else:
            client_socket.send('File does not exist'.encode())
            print("File not found")
