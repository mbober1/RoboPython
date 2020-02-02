import time, constant, pygame, os
from socket import *


class Client():
    def __init__(self):
        self.connected = False
        self.s = socket()
        self.ping_sum = 0
        self.ping_count = 0

    def __del__(self):
        if self.ping_count > 0: print("Average ping: ", round(((self.ping_sum/self.ping_count)*1000),1), 'ms')
        
        if self.connected: 
                self.send_data("close")
                self.s.close()
                print("Connection closed")

        
    def connect(self):
        self.s.connect(("bobermarcin.pl", constant.PORT))
        print('Connected to ', constant.HOST, ':', constant.PORT)
        self.connected = True
        print('Start sending data...')
        
    def send_data(self, data=''):
        self.s.sendall(data.encode())

    def receive_data(self):
        return (self.s.recv(2000)).decode()


        