from Thread import Runner
from System import read

import time
import math 

class Motor(Runner):
    def __init__(self,Pin):
        super(Motor,self).__init__([Pin])
    def init(self,Pin):
        self.Pin = Pin
        self.pin = [[25,24],[20,21]]
        self.json = read("speed.json")
        for i in range(2):
            for j in range(2):
                Pin.setup(self.pin[i][j],Pin.OUT)
    def rotate(self, orientation1, orientation2, l,t,s=1):
        wait = self.calc(l,t)
        self.Pin.output(self.pin[0][0], s*(1-orientation1))
        self.Pin.output(self.pin[0][1], s*orientation1)
        self.Pin.output(self.pin[1][0], s*(1-orientation2))
        self.Pin.output(self.pin[1][1], s*orientation2)
        if wait > 0: time.sleep(wait)
    def stop(self,l = 0): self.rotate(1,1,l,"s",0)
    def front(self,l = 0): self.rotate(1,1,l,"v1",1)
    def back(self, l = 0): self.rotate(0,0,l ,"v2",1)
    def right(self, l = 0):  self.rotate(0,1,l,"w1",1)
    def left(self, l = 0):  self.rotate(1,0,l,"w2",1)
    def calc(self,l,t): # Transform distance (cm/º) to time (s)
        if l == 0: return 0
        if t == "s": return 0
        if "w" in t: return math.pi*l*self.json[t][0]/180+self.json[t][1]
        return l*self.json[t][0]+self.json[t][1]
    def calc_inv(self,l,t): # Transform time to distance
        if t == "s": return 0
        if "w" in t: return (l-self.json[t][1])*180/self.json[t][0]/math.pi
        return (l-self.json[t][1])/self.json[t][0]

if __name__ == "__main__":
    import RPi.GPIO as Pin
    Pin.setwarnings(False)
    Pin.setmode(Pin.BCM)
    motor = Motor(Pin)
    Motor.wait()
    motor.front(100)
    motor.stop()