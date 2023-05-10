from indexer.indexer_utils import *
from concurrent.futures import ThreadPoolExecutor


class Indexer:
    data_structure = RoutingInfoDataStructure()

    def __init__(self):
        self.active_connections:dict = {}


    def threadHandler(self, client_socket:socket.SocketType, client_address):
        requestTypes:dict = {
            "makeFilePublic": self.indexReceivedPublicFiles,
            "searchFile": self.returnSearchedFiles
        }

        # Read the client request and handle it
        data = client_socket.recv(BUFFER_SIZE).decode().strip()
        print(f'Received request: {data}')

        id, request_type = data.split()

        self.active_connections.setdefault(id, '').extend(client_address[0])
        print(self.active_connections)

        if request_type in requestTypes:
            requestTypes[request_type](client_socket, id)


    def startIndexer(self):
        try:

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((SERVER_ADDR, PORT))
            server_socket.listen()
            print('Listening for incoming connections...')

            while True:
                client_socket, client_address = server_socket.accept()
                executor = ThreadPoolExecutor(max_workers=10)
                executor.submit(self.threadHandler, client_socket, client_address)

        except socket.error as error:
            print(error)
    

    def indexReceivedPublicFiles(self, client_socket:socket.SocketType, id):
        num_of_files:int = int(
            client_socket.recv(BUFFER_SIZE).decode())
        print(f'{num_of_files} files to be indexed')

        files_to_be_indexed:list[str] = []
        
        for i in range(num_of_files):
            data = client_socket.recv(BUFFER_SIZE).decode()
            print(data)
            files_to_be_indexed.append(data)
            
        self.data_structure.createDataStructure(files_to_be_indexed, id)
        print(self.data_structure.shared_files_info)

        client_socket.close()


    def returnSearchedFiles(self, client_socket:socket.SocketType, id):
        file_name:str = client_socket.recv(BUFFER_SIZE).decode()

        result:None or list(str) = self.data_structure.search(file_name)
        
        if result:
            available_client_addresses:list[str] = []

            for id in result:
                if id in self.active_connections:
                    available_client_addresses.append(self.active_connections[id])

            for address in available_client_addresses:
                client_socket.send(address.encode())
                print("File found")
        else:
            client_socket.send('File does not exist'.encode())
            print("File not found")