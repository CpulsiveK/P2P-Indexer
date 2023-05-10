from _thread import *
import socket

SERVER_ADDR:str = socket.gethostbyname(socket.gethostname())
print(SERVER_ADDR)
PORT:int = 5050

class RoutingInfoDataStructure:
    shared_files_info:dict = {}
    
    def createDataStructure(self, files:list[str], id:str) -> None:
        id_found:bool = False
    
        for file in files:
            for id in self.shared_files_info:
                if id == id:
                    self.shared_files_info[id].append(file)
                    id_found = True
        
        if not id_found:
            self.shared_files_info[id] = files
    

    def search(self, filename:str) -> list[str]:
        ids_of_files_found = []

        for id in self.shared_files_info:
            for file in self.shared_files_info[id]:
                if file[0] == filename:
                    ids_of_files_found.append(id)
        
        if len(ids_of_files_found) == 0:
            return None
        else:
            return ids_of_files_found