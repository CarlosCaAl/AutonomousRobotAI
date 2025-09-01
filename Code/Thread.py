import threading
import time

# Threads have 2 uses in this code:
# 1. Run secondary actions parallelly to save time
# 2. Do several actions at the same time

def Run(func):
    Thread(func=func,start=1)

class Runner(): # Parallelly starts objects
    def __init__(self, param=None):
        self.started = 0
        self.runner = Thread(self.run, param=param, start=1)
    def run(self, *args):
        self.init(*args)
        self.started += 1
    def wait(self):
        while self.started != 1:
            time.sleep(0.1)

class Thread(threading.Thread): # Create a thread
    def __init__(self,func,param=None,loop=False,var=None,sleep=0,start=0):
        super(Thread,self).__init__()
        self.interations = 0
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
        self.func = func
        self.loop = loop
        self.param = param
        self.var = var
        self.sleep = sleep
        self._stop_event = threading.Event()
        if start: 
            self.start()
            if loop == False:
                self.stop()
    def run(self): # Run function structure
        self.resume()
        if self.loop == True:
            while True:
                with self.state:
                    if self.paused: self.state.wait()
                time.sleep(self.sleep)
                self.runFunc()
        else: 
            self.runFunc()
            self.stop()
        self.interations += 1
    def runFunc(self): # Run function once
        if self.param == None: n = self.func()
        elif len(self.param) == 1: n = self.func(self.param[0])
        elif len(self.param) == 2: n = self.func(self.param[0],self.param[1])
        elif len(self.param) == 3: n = self.func(self.param[0],self.param[1],self.param[2])
        elif len(self.param) == 4: n = self.func(self.param[0],self.param[1],self.param[2],self.param[3])
        elif len(self.param) == 5: n = self.func(self.param[0],self.param[1],self.param[2],self.param[3],self.param[4])
        elif len(self.param) == 6: n = self.func(self.param[0],self.param[1],self.param[2],self.param[3],self.param[4],self.param[5])
        if self.var is not None and n is not None: self.var.write(n)
    def pause(self): # Pause thread
        with self.state:
            self.paused = True
    def resume(self): # Resume thread
        with self.state:
            self.paused = False
            self.state.notify()
    def stop(self): # Stop thread
        self.pause()
        self._stop_event.set()

class Variable: # Variable accessible from any line to transfer data between threads
    def __init__(self,val=None): self.val = val
    def write(self,val): self.val = val
    def read(self): return self.val