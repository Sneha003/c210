# -----------Bolierplate Code Start -----


import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import filedialog


PORT = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096
name = None
labellost = None
textarea = None
textMessage = None
labelChat = None

def connectWithClient():
    global SERVER
    global labellost

    textMessage=labellost.get(ANCHOR)
    list_item = textMessage.split(":")
    msg="connect "+list_item[1]
    SERVER.send(msg.encode('ascii'))

def disconnectWithClient():
    global SERVER
    global labellost

    textMessage=labellost.get(ANCHOR)
    list_item = textMessage.split(":")
    msg="disconnect "+list_item[1]
    SERVER.send(msg.encode('ascii'))



def recvMessage():
    global SERVER
    global BUFFER_SIZE
    while True:
        chunk = SERVER.recv(BUFFER_SIZE)
        try:
            if("tiul" in chunk.decode() and "1: " in chunk.decode()):
                letter_list = chunk.decode().split(",")
                labellost.insert(
                    letter_list[0], letter_list[0]+":"+letter_list[1]+":"+letter_list[3]+":", letter_list[5])
                print(letter_list[0], letter_list[0]+":" +
                      letter_list[1]+":"+letter_list[3]+":", letter_list[5])
            else:
                textarea.insert(END, "\n"+chunk.decode("ascii"))
                textarea.see("end")
                print(chunk.decode("ascii"))

        except:
            pass

def showClientList():
    global labellost
    labellost.delete(0,"end")
    SERVER.send("showList".encode("askcii"))




def connectToServer():
    global send_file
    global name
    global SERVER
    client_name=name.get()
    SERVER.send(client_name.encode())



def Openchatwindow():
    global name
    global labellost
    global textMessage
    global textarea
    global filePathLable
    
    window = Tk()
    window.title("messenger")
    window.geometry("500x350")

    namelabel = Label(window, text="enter your name", font=("calibri", 10))
    namelabel.place(x=10, y=10)

    name = Entry(window, width=30, font=("Calibri", 10))
    name.place(x=120, y=10)
    name.focus()

    Connectserver = Button(
        window, text="connect to the chat server", bd=1, font=("calibri", 10),command=connectToServer)
    Connectserver.place(x=350, y=15)

    separator = ttk.Separator(window, orient="horizontal")
    separator.place(x=0, y=35, relwidth=1, height=0.1)

    labelUsers = Label(window, text="active users", bd=1, font=("calibri", 10))
    labelUsers.place(x=10, y=50)

    labellost = Listbox(window, height=5, width=67,
                        activestyle="dotbox", font=("calibri", 10))
    labellost.place(x=10, y=70)

    Scrollbar1 = Scrollbar(labellost)
    Scrollbar1.place(relheight=1, relx=1)
    Scrollbar1.config(command=labellost.yview)

    connect = Button(window, text="connect", bd=1, font=("calibri", 10),command=connectWithClient)
    connect.place(x=282, y=160)

    disconnect = Button(window, text="disconnect", bd=1, font=("calibri", 10),command=disconnectWithClient)
    disconnect.place(x=352, y=160)

    refresh = Button(window, text="refresh", bd=1, font=("calibri", 10),command=showClientList)
    refresh.place(x=435, y=160)

    labelChat = Label(window, text="chat window", bd=1, font=("calibri", 10))
    labelChat.place(x=10, y=180)

    textarea = Text(window, width=67, height=6, font=("calibri", 10))
    textarea.place(x=10, y=200)

    attach = Button(window, text="attach & send", bd=1, font=("calibri", 10))
    attach.place(x=10, y=300)

    textMessage = Entry(window, width=43, font=("Calibri", 12))
    textMessage.place(x=98, y=300)
    textMessage.focus()

    send = Button(window, text="send", bd=1, font=("calibri", 10))
    send.place(x=450, y=300)

    filePathLable = Label(window, text="", bd=1,
                          font=("calibri", 8), fg="blue")
    filePathLable.place(x=10, y=330)

    Scrollbar2 = Scrollbar(labellost)
    Scrollbar2.place(relheight=1, relx=1)
    Scrollbar2.config(command=labellost.yview)

    window.mainloop()


def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    Openchatwindow()


setup()


# -----------Bolierplate Code Start -----
