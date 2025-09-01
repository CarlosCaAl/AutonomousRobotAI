from Thread import Runner,Run

from adafruit_motor import servo
from board import SCL, SDA
from colorama import Fore
import adafruit_pca9685
import busio
import time 

class Servo(Runner):
    def __init__(self):
        super(Servo,self).__init__(None)
    def init(self):
        self.available = True
        try:
            bus = busio.I2C(SCL, SDA)
            pca = adafruit_pca9685.PCA9685(bus)
            self.pca = pca
            pca.frequency = 60
            self.servos = []
            self.mem = []
            self.sleep = [90,90,90,90,90,90,90,90,90,90]
            for i in range(10):
                self.mem.append(90)
                self.servos.append(servo.Servo(pca.channels[i],min_pulse=500,max_pulse=2400))
                self.angle(i,90)
        except Exception as e: 
            self.available = False
            print(Fore.MAGENTA+"ERROR:"+Fore.WHITE+" Servo controller disconnected")
    def stop(self,s): # Disable all motors
        time.sleep(10)
        self.angle(s,None)
    def angle(self,s,a,reg=True): # Move a servo to an angle
        if a is not None:
            if a > 180: a = 180
            if a < 0: a = 0
        if self.available: 
            self.servos[s].angle = a
            if a is None: self.pca.channels[s].duty_cicle = 0
            if a == 90: Run(lambda:self.stop(s))
            if reg: # Register the actual angle
                self.mem[s] = a if a is not None else 90
            time.sleep(0.2)
    def set(self,state,sleep): # Establish a value for each servo
        for i in range(10): 
            self.angle(i,state[i])
        time.sleep(sleep)
    def move(self,state,t): # Move at the same time the servos to a position
        servos = [i for i in range(10) if state[i] is not NotImplemented]
        r = [state[i]-self.mem[i] for i in servos]
        for i in range(int(100*t)):
            for j in servos: self.angle(j,self.mem[j]+r[servos.index(j)]*(i+1)/t/100,reg=False)
            time.sleep(.01)
        for i in range(10):
            if state[i] != None: self.mem[i] = state[i]
    def simetric_move(self,state,t): # Move at the same time the servos when both arms move simetrically
        for i in range(2,6): 
            state.append(180-state[i])
        self.move(state,t)
        