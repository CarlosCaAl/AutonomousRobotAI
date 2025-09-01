import time
from Thread import Runner

class Ultrasonic(Runner):
    def __init__(self,Pin,tpin=14,epin=15):
        super(Ultrasonic,self).__init__((Pin,tpin,epin))
    def init(self,Pin,tpin=14,epin=15):
        self.Pin = Pin
        self.trigPin = tpin
        self.echoPin = epin
        Pin.setup(self.trigPin,Pin.OUT)
        Pin.setup(self.echoPin,Pin.IN)
        Pin.output(self.trigPin,False)
    def readAction(self,d=2):
        self.Pin.output(self.trigPin,True)
        time.sleep(0.00001)
        self.Pin.output(self.trigPin,False)
        time0 = time.time()
        while self.Pin.input(self.echoPin) == 0:
            if time.time() - time0 > .1: break
        time1 = time.time()
        while self.Pin.input(self.echoPin) == 1: pass
        r = (time.time()-time1)/0.000058
        if r > 1200: _,r = time.sleep(.01),self.readAction(d)
        return r
    def read(self, d=2, r=5): # Get distance
        s = 0
        for i in range(r):
            time.sleep(.01)
            s += self.readAction()/r
        return round(s,d)
    
if __name__ == "__main__":
    import RPi.GPIO as Pin
    Pin.setwarnings(False)
    Pin.setmode(Pin.BCM)
    ultrasonic = Ultrasonic(Pin)
    ultrasonic.wait()
    while True:
        print(ultrasonic.read())
        time.sleep(.2)