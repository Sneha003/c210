# ------- Bolierplate Code Start -----


from base64 import encode
from concurrent.futures import thread
from http import server
import socket

from threading import Thread
import time


IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}



def handleshowList(client):
    global clients
    counter=0
    
    for c in clients :
        counter+=1
        client_address=clients[c]["address"][0]
        connected_with_whom =clients[c]["connected_with_whom"]
        message= ""
        if(connected_with_whom):
            message=f"{counter},{c},{client_address},connected_with{connected_with_whom}"
        else:
            message=f"{counter},{c},{client_address},available"
        client.send(message.encode())
        time.sleep(1)

            

def connectClient(message, client, client_name):
    global clients
    print(message)
    enterClientName=message[8:].strip()

    if(enterClientName in clients):

        clients[enterClientName]["connected_with_whom"]=client_name
        
        clients[client_name]["connected_with_whom"]=client_name
        otherClientSocket=clients[enterClientName]["client"]
        greetingmessage=f"hello,{enterClientName}you are sucessfully connected with {client_name}"
        otherClientSocket.send(greetingmessage.encode())
        greetingmessage2=f"you are sucessfully connected with{enterClientName}"
        client.send(greetingmessage2.encode())
    
    else:
        otherClientName=clients[client_name]["connected_with_whom"]
        greetingmessage2=f"you are already connected with{otherClientName}"
        client.send(greetingmessage2.encode())

        
    

def disconnectClient(message, client, client_name):
    global clients
    print(message)
    enterClientName=message[11:].strip()

    if(enterClientName in clients):
        clients[enterClientName]["connected_with_whom"]=""
        clients[client_name]["connected_with_whom"]=""
        otherClientSocket=clients[enterClientName]["client"]
        greetingmessage=f"hello,{enterClientName}you are sucessfully disconnected with {client_name}"
        otherClientSocket.send(greetingmessage.encode())
        greetingmessage2=f"you are sucessfully disconnected with{enterClientName}"
        client.send(greetingmessage2.encode())

def handleMessages(client,message,client_name):
    if(message=="show list"):
        handleshowList()
    elif(message[:7]=="connect"):

        connectClient(message,client,client_name)

    elif(message[:10]=="disconnect"):
        disconnectClient(message,client,client_name)

def handleClient(client,client_name):
    global clientS
    global SERVER
    global BUFFER_SIZE

    welcomeMessage="welcome,you are connected to a server\nclick on refresh to see the available users\nselect the user and click on connect button to start chatting"
    client.send(welcomeMessage,encode())
    
    while True:
        try:
            BUFFER_SIZE=clients[client_name]["file size"]
            chunck=client.recv(BUFFER_SIZE)
            message=chunck.decode().strip().lower()
            if message:
                handleMessages(client,message,client_name)

        except:
            pass

    
        



def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        print(client, addr)
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {

            "client": client, "address": addr, "connected_with_whom": "", "file_name": "", "file_size": ""
        }


        print("\n\t\t\t\t\t")
        print(f"connection established with{client_name}:{addr}")
        thread=Thread(target=handleClient,args=(client,client_name))
        thread.start()


def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup_thread = Thread(target=setup)  # receiving multiple messages
setup_thread.start()

# ------ Bolierplate Code End -----------
