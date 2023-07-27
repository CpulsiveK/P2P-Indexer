# P2P-Indexer
This repository contains the server side code for the Peer-to-Peer Multimedia Sharing Application repo

# Start the indexer
To run the code simply go to the commandline and cd into src directory and run this command: 
'python main.py' 

or simply run :

'python src/main.py'

NB: python 3 or higher required

Once you see the below printed on the console, it means the server is running.

"[INDEXER]: 'your local ip' is listening on [PORT]: 5050 for incoming connections...
Listening for new nodes"


# How to integrate indexer

## Indexing
The class "RoutingInfoDataStructure" contains a method called "createDataStructure" and this method is what is responsible for indexing. There is only one instance of the class for which all file information is currently stored in memory. 

The files information is indexed on the server in a dictionary with the id of the sender as key and the file information as value.

The value is another dictionary with the file name as key and file path as value.
Eg:
shared_files_info:dict = {
    "id": {
        "filename": "path/to/file"
    }
}

## Server ip broadcast
The "unicastIndexerAddr()" function listens for incoming connections from peers and sends it's current ip on message "indexer ip?" received. This allows peers to be updated on any ip change from the server side.
This implementation is flawed in many ways and will be improved.

NB:
The initial ip of the server on first time configuration on the local network must be hardcoded in your app


## Request handlers
The "Indexer" class has methods for handling requests, which are: 
"makeFilePublic"
"searchFile"

To access any of these requests, a request type must be sent to the indexer upon connection to the server where the server looks up its "requestTypes" dictionary to see if it exists and calls the associated method to handle the request. Here is the "requestTypes" dictionary:

requestTypes: dict = {
            "makeFilePublic": self.     indexReceivedPublicFiles,
            "searchFile": self.returnSearchedResult,
        }

Each request type method has a set of parameters it expects and either sends a response back to the peer or not.

For "searchFile" requestype it only needs the socket the peer connected with:
def returnSearchedResult(self, client_socket: socket.SocketType)
On completion of the request a response containing a list of json string enconded dictionary of current ip addresses of file info owners mapped to their filepaths.
eg:
[
    "{"192.168.49.103": "path/to/file}",
    "{"192.168.49.103": "path/to/file}"
]
This information can be decoded on the frontend and the key (ip) used to connect to the specific peer with the file and initiate a download by sending the value (file path).

For "makeFilePublic" request type it needs an extra parameter which is the id of the peer making the request and does not send any response back to the peer ie
def indexReceivedPublicFiles(self, client_socket: socket.SocketType, id)










