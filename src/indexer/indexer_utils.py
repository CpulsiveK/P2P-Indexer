import socket

SERVER_ADDR:str = socket.gethostbyname(socket.gethostname())
print(SERVER_ADDR)
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
        