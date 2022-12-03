# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 21:18:15 2022

@author: DELL
"""
import socket
import threading

host="127.0.0.1" #local address
port=55555
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host,port))
server.listen()
clients=[]
names=[]
def broadcast(mesg):
    for clt in clients:
        clt.send(mesg) 
        
def handle(clt):
    while True:
        try:
            msg=clt.recv(1024)
            broadcast(msg)
        except:
            index=clients.index(clt)
            clients.remove(clt)
            clt.close()
            nickname=names[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            names.remove(nickname)
            break
def receive():
    while True:
        clt, address= server.accept()
        print(f'Connected with{str(address)}')
        clt.send('nickname'.encode('ascii'))
        nickname=clt.recv(1024).decode('ascii')
        names.append(nickname)
        clients.append(clt)
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} is connectes'.encode('ascii'))
        clt.send('Connected to the server!'.encode('ascii'))
        thread=threading.Thread(target=handle,args=(clt,))
        thread.start()
        
print('-server is working...')        
receive()
    