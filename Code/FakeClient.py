from Thread import Thread,Runner
import time

class Client(Runner): # Fake client for the offline mode
    def __init__(self,app=None,func=None,func2 = None,func3 = None):
        super(Client,self).__init__((app,func,func2,func3))
    def init(self,app=None,func=None,func2 = None,func3 = None):
        self.func = func
        self.func2 = func2
        self.func3 = func3
        self.app = app
        self.state = 1
        self.recvVideo()
        self.videoThread = Thread(self.recvVideo,loop=True)
        self.videoThread.start()
        self.video = 0
    def send(self,msg): self.func2(msg) # Send a message to the server (in this fake mode, to the main function)

    def toogleVideo(self):
        if self.videoThread.paused == False: self.videoThread.pause()
        else: self.videoThread.resume()
    
    def reset(self):
        self.app.clientIsOpen = 0
        self.state = -1

    def recvVideo(self): # Receive video and insert it
        if self.state == 1:
            try: self.videoFunc()
            except:
                self.videoFunc()
                self.reset()
    def videoFunc(self):
        try: 
            frame = self.func3() # receive the video
            self.func(frame) # insert the video
            time.sleep(1)
        except: pass
