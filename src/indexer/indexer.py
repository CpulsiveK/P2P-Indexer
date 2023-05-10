from indexer.indexer_utils import *
import threading


class Indexer:
    data_structure = RoutingInfoDataStructure()

    def __init__(self):
        self.active_connections:dict = {}


    def threadHandler(self, client_socket:socket.SocketType, client_address):
        requestTypes = {
            "makeFilePublic": self.indexReceivedPublicFiles,
        }

        # Read the client request and handle it
        data = client_socket.recv(1024).decode().strip()
        print(f'Received request: {data}')

        id, request_type = data.split()

        if request_type in requestTypes:
            requestTypes[request_type](client_socket, id)


    def startServer(self):
        try:

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((SERVER_ADDR, PORT))
            server_socket.listen()
            print('Listening for incoming connections...')

            while True:
                client_socket, client_address = server_socket.accept()
                thread = threading.Thread(target=self.threadHandler, args=(client_socket, client_address))
                thread.start()
                print("[ACTIVE CONNECTIONS] ", threading.active_count() - 1)

        except socket.error as error:
            print(error)
    

    def indexReceivedPublicFiles(self, client_socket:socket.SocketType, id):
        num_of_files = int(
            client_socket.recv(1024).decode())
        print(f'{num_of_files} files to be indexed')

        files_to_be_indexed = []
        
        for i in range(num_of_files):
            data = client_socket.recv(1024).decode()
            print(data)
            files_to_be_indexed.append(data)
            
        self.data_structure.createDataStructure(files_to_be_indexed, id)
        print(self.data_structure.shared_files_info)

        client_socket.close()