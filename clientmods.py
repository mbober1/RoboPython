import constant
from socket import *


class Client():
    def __init__(self):
        self.connected = False
        self.s = socket()

    def __del__(self):
        if self.connected: 
                self.send_data("close")
                self.s.close()
                print("Connection closed")

        
    def connect(self):
        print('Connecting...')
        self.s.connect((constant.HOST, constant.PORT))
        print('Connected to ', constant.HOST, ':', constant.PORT)
        self.connected = True
        print('Start sending data...')
        
    def send_data(self, data=''):
        str_data = str(data)
        self.s.sendall(str_data.encode())
        # print(str_data)

    def receive_data(self):
        return (self.s.recv(2000)).decode()


        