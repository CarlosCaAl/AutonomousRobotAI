from Thread import Thread,Runner
from System import read

import socket
import pickle
import struct
from rpi_ws281x import Color
import time as t
import cv2 as cv
from colorama import Fore

class Server(Runner):
    def __init__(self,cam,scr,voice,func,host=None,a=1):
        super(Server,self).__init__((cam,scr,voice,func,host,a))
    def init(self,cam,scr,voice,func,host=None,a=1): # Start server
        if host == None: host = read("data.json")["ip"]
        self.func = func
        port1,port2 = 8000,8888  
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((host,port1))
            port = port1
        except:
            try:
                self.server.bind((host,port2))
                port = port2
            except: 
                if a: 
                    print(Fore.MAGENTA+"ERROR:"+Fore.WHITE+" Server failure, solve this issue: https://carloscaal.eu.pythonanywhere.com/errores?error=error01")
                    port = 1000
        self.a = a
        self.server.listen()
        self.cam,self.scr = cam,scr
        if a: self.voice = voice
        if port != 1000: self.host,self.port = host,port
        self.client = None

    def connect(self): # Listen to connections
        a = self.a
        if a: print(Fore.BLUE+" RPI4:"+Fore.WHITE+" Server opened --> {}:{}".format(self.host,self.port))
        self.adress = None
        self.client,self.adress = self.server.accept()
        print(Fore.BLUE+" RPI4:"+Fore.WHITE+' Client connected: {}'.format(str(self.adress)))
        self.scr.text(" ",fg=Color(0,200,100))
        t.sleep(2)
        self.scr.show(self.scr.letters[47].paint(Color(0,200,100)))

    def send(self,msg,cliente): cliente.send(msg.encode('utf-8'))
    def recv(self,cliente): return cliente.recv(1024).decode('utf-8')

    def sendVideo(self): # Send video to client
        frame = self.cam.read()
        frame = cv.resize(frame,(120,90),interpolation = cv.INTER_CUBIC)
        a = pickle.dumps(frame)
        self.client.sendall(struct.pack("Q",len(a))+a)

    def start(self,end): # Start loop listening to the client
        self.end = end
        self.recvThread = Thread(func=self.recvLoop,loop=True)
        self.recvThread.start()

    def recvLoop(self):
        if self.client == None: self.connect()
        r = self.recv(self.client)
        if r == 'close': 
            print(Fore.BLUE+" RPI4:"+Fore.WHITE+'Client disconnected')
            self.connect()
        elif r == 'end': 
            print(Fore.BLUE+" RPI4:"+Fore.WHITE+'Client forced ending the code')
            self.end.write(1)
        elif r == 'video':
            self.sendVideo()
            t.sleep(0.2)
        elif r != '': n = self.func(r)
