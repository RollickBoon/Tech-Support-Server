import socket
import select
import sys
import time
from tkinter import *
from threading import *
from uuid import getnode as get_mac

def send_msg(event=None):
        message = ENTRY.get()
        my_msg.set("")
        server.send(message.encode())

def recv_msg(sock):
    while True:
        message = sock.recv(2048)
        TXT.config(state=NORMAL)
        print(message.decode())
        TXT.insert(END, message.decode())
        TXT.insert(END, '\n')
        TXT.config(state=DISABLED)
        TXT.see("end")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "192.168.0.17"
# ip_address = socket.gethostbyname(socket.getfqdn())
Port = 5001
mac = get_mac()
hash = "##"
mac_str = hash + str(mac) + hash
print(mac_str)
print(str(mac_str)[0] + str(mac_str)[1] + str(mac_str)[-2] + str(mac_str)[-1])
server.connect((ip_address, Port))
sockfd.connect((ip_address, Port))
time.sleep(1)
server.send(mac_str.encode())

root = Tk()
root.title("Tech Support")
my_msg = StringVar()

L = Label(root, text="Tech Support Chatroom", font=("Courier", 20), pady=10)
L.grid(row=0)
TXT = Text(root, width=100, font=("Courier", 12))
TXT.grid(row=1, column=0, sticky=E, padx=(10,0))
S = Scrollbar(root)
S.config(command=TXT.yview)
S.grid(row=1, column=1, sticky=NSEW)
TXT.config(yscrollcommand=S.set)
ENTRY = Entry(root, width=75, textvariable=my_msg, font=("Courier", 12))
ENTRY.bind("<Return>", send_msg)
ENTRY.grid(row=2, pady=(10,0))
ENTRY.focus_set()
B = Button(root, text="Send", command=send_msg, font=("Courier", 12))
B.grid(row=3, pady=10)

Thread(target=recv_msg, args=(sockfd,)).start()
# Thread(target=send_msg, args=(server,)).start()

root.mainloop()
