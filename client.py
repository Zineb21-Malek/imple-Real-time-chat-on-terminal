"""
Created on Sat Dec  3 08:08:09 2022

@author: DELL
"""

import socket
import threading


nickname=input('Enter yor nickname: ')
clt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clt.connect(('127.0.0.1',55555))


def receive():
    while True:
        try:
            msg=clt.recv(1024).decode('ascii')
            if msg=='nickname':
                clt.send(nickname.encode('ascii'))
                
            else:
                print(msg)
        except:
            print('ERROR !!!')
            clt.close()
            break
        
def write():
    while True:
        msg=f'{nickname}: {input("")}'
        clt.send(msg.encode('ascii'))
            
receive_thread=threading.Thread(target=receive)
receive_thread.start()
write_thread=threading.Thread(target=write)
write_thread.start()







    