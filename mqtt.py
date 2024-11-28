import sys
import random
import time
import socket
from collections import namedtuple
#pip install adafruit-io
from Adafruit_IO import MQTTClient
from Adafruit_IO import Client,Feed
#pip install pyserial
import serial.tools.list_ports
import threading

class AdaFruitMQTT:
    def initAdafruit(self,username, key):
        self.aio = Client(username,key)
        self.client = MQTTClient(username,key)
        self.feed_id_list = self.aio.feeds()
        print(self.feed_id_list)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
    def initSocket(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.bind(('localhost',2703))
        self.sock.listen(5)
    def __init__(self, username, key):
        print("OK")
        self.ser = None
        self.mess = ""
        self.request = ""
        self.initAdafruit(username, key)
        self.initSocket()
        self.client.connect()
        self.client.loop_background()
        while True:
            self.listen()

    def connected (self,client):
        print ("Ket noi thanh cong ...")
        for feed in self.feed_id_list:
            client.subscribe(feed)

    def subscribe (self,client,userdata,mid,granted_qos):
        print ("Subcribe thanh cong ...")

    def disconnected (self,client) :
        print ("Ngat ket noi ...")
        sys.exit(1)

    def message (self,client,feed_id ,payload):
        print ("Nhan du lieu : " + payload)

    def processData(self,data):
        data = data.replace("!", "")
        data = data.replace("#", "")
        splitdata = data.split(":")
        #Phần request bên backend sẽ là: !REQUEST ACTION VALUE#
        #Ví dụ như kéo cái thanh trượt hay bấm nút(Đại loại v)
        if splitdata[0] == "REQUEST":
            if splitdata[1] == "DUMMY":
                print(splitdata[2])
                pass


    def listen(self):
        client_sock, addr = self.sock.accept()
        self.request += client_sock.recv(1024).decode()
        if self.request != "":
            while ('#' in self.request) and ('!' in self.request):
                start = self.request.find('!')
                end = self.request.find('#')
                self.processData(self.request[start:end+1])
                if (end == len(self.request)):
                    self.request = ""
                else:
                    self.request = self.request[end+1:]
        msg = "cam on" + str(addr)
        client_sock.send(msg.encode())
        client_sock.close()
    

AIO_USERNAME = "k245416587" #Tên 
AIO_KEY = "aio_XdCd95ltIngtMWkPBK0AhqbKdhYY"

adafruit_mqtt = AdaFruitMQTT(AIO_USERNAME, AIO_KEY)
