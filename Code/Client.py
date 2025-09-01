from Thread import Thread

import socket
import time
import cv2 as cv
import pickle
import struct
import webbrowser

class Client:
    def __init__(self,ip=None,app=None,func=None):
        self.func = func
        self.app = app
        self.state = 1
        self.host,self.port1,self.port2 = ip,8000,8888
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
    def connect(self):
        c = 0
        for i in range(3):
            try:
                self.client.connect((self.host,self.port1))
                c = 1
                break
            except:
                time.sleep(0.5)
                try:
                    self.client.connect((self.host,self.port2))
                    c = 1
                    break
                except: time.sleep(0.5)
        if c == 0:
            print("ERROR: visit https://carloscaal.eu.pythonanywhere.com/errores?error=error01")
            webbrowser.open("https://carloscaal.eu.pythonanywhere.com/errores?error=error01")
    def recv(self):
        try:
            msg = self.client.recv(1024).decode('utf-8')
            print(msg)
            return msg
        except:
            self.client.close()
            return "error"

    def send(self,msg):
        try: self.client.send(msg.encode('utf-8'))
        except: self.reset()

    def toogleVideo(self):
        if self.videoThread.paused == False: self.videoThread.pause()
        else: self.videoThread.resume()
    
    def reset(self):
        self.app.clientIsOpen = 0
        self.state = -1

    def recvVideo(self):
        if self.state == 1:
            try: self.videoFunc()
            except:
                self.videoFunc()
                self.reset()
    def videoFunc(self):
        size = struct.calcsize("Q")
        self.send('video')
        data = b""
        while len(data) < size:
            packet = self.client.recv(4*1024)
            if not packet: break
            data += packet
        msgSize1 = data[:size]
        data = data[size:]
        msgSize2 = struct.unpack("Q",msgSize1)[0]
        while len(data) < msgSize2: data += self.client.recv(4*1024)
        frameData = data[:msgSize2]
        frame = pickle.loads(frameData)
        frame = cv.resize(frame,(640,480),interpolation=cv.INTER_CUBIC)
        self.func(frame)
        cv.imshow("Camera",frame)
        time.sleep(1)
        pass
