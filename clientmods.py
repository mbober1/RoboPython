import time, constant, pygame, os
from socket import *


class Client():
    def __init__(self):
        self.s = socket()
        self.ping_sum = 0
        self.ping_count = 0

    def __del__(self):
        if self.ping_count > 0: print("Average ping: ", round(((self.ping_sum/self.ping_count)*1000),1), 'ms')
        self.send_data("close")
        self.s.close()

    def connect(self):
        self.s.connect(("bobermarcin.pl", constant.PORT))
        print('Connected to ', constant.HOST, ':', constant.PORT)
        print('Start sending data...')
        
    def send_data(self, data=''):
        self.s.sendall(data.encode())

    def receive_data(self):
        return (self.s.recv(2000)).decode()

    def ping(self):
        response = os.system("ping -c 1 " + "192.168.0.71")
        print(response)
        # time1 = time.time()
        # self.send_data('ping')
        # self.receive_data()
        # self.ping_sum = self.ping_sum + time.time() - time1
        # self.ping_count = self.ping_count+1 
        # print('ping: ', round(((time.time() - time1)*1000),1), 'ms')



        