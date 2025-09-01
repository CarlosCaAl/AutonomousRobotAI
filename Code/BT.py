from Math import t
from System import read, os
from Thread import Thread,Variable,Runner, Run

from pyPS4Controller.controller import Controller
from rpi_ws281x import Color
from colorama import Fore
import bluetooth
import time

IP = read("bt.json")

class BT(Runner):
    def __init__(self,ip=IP["arm"],port=1):
        super(BT,self).__init__((ip,port))
    def init(self,ip=IP["arm"],port=1):
        try:
            self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.sock.connect((ip,port))
            print(Fore.BLUE+" RPI4: "+Fore.WHITE+f"Robotic arm connected through bluetooth")
        except: print(Fore.MAGENTA+"ERROR: "+Fore.WHITE+f"Robotic arm disconnected")
    def send(self, msg):
        self.sock.send(msg)
    def recv(self):
        return self.sock.recv(1024)

class Arm(BT):
    def __init__(self,ip=IP["arm"],port=1):
        self.A = 24
        self.B = 77
        self.C = 148
        super(Arm,self).__init__(ip=IP["arm"],port=1)
    def init(self,ip=IP["arm"],port=1):
        super(Arm,self).init(ip=ip,port=1)
    def servo(self,n,angle):
        try:
            a = str(angle)
            if angle < 100: 
                a = "0" + a
                if angle < 10: a = "0" + a
            self.send(str(n)+a)
        except: pass
    def sleep(self):
        for i in range(4): self.servo(i+1,90)
    def coord2angle(self,p):
        X,Y,Z = -p[0],p[1],p[2]
        a = 90 + t.Atan(X/Y)
        Y -= self.A
        R = t.sqrt(t.sq(X)+t.sq(Y))
        T = t.sqrt(t.sq(R)+t.sq(Z))
        b = t.Acos((t.sq(self.B)+t.sq(self.C)-t.sq(T))/(2*self.B*self.C))
        c = 180 - t.Atan(Z/R) - t.Acos((t.sq(self.B)+t.sq(T)-t.sq(self.C))/(self.B*T*2))
        return a,90+b-c,c
    def go_to(self, coord):
        a,b,c = self.coord2angle(coord)
        self.servo(3,int(10+c))
        self.servo(2,int(5+b))
        self.servo(4,int(a))
    def grab(self,coord):
        r1 = t.sqrt(t.sq(coord[0])+t.sq(coord[1]))
        r2 = r1 - 20
        self.go_to((r2/r1*coord[0],r2/r1*coord[1],coord[2]))
        time.sleep(1)
        self.go_to(coord)
        time.sleep(1)
        self.servo(1,30)
    def release(self,coord):
        self.go_to(coord)
        time.sleep(1)
        self.servo(1,90)
        r1 = t.sqrt(t.sq(coord[0])+t.sq(coord[1]))
        r2 = r1 - 40
        time.sleep(1)
        self.go_to((r2/r1*coord[0],r2/r1*coord[1],coord[2]))

if __name__ == "__main__":
    arm = Arm()
    while True:
        try: arm.go_to([int(i) for i in input("Type coordinates (x y z): ").split()])
        except: break



class MyController(Controller):

    def __init__(self, func, ip, **kwargs):
        self.func = func
        self.ip = ip
        Controller.__init__(self, **kwargs)
        self.joystick = [0,0]
        self.process = {"joystick":{"L4":"m1","L1":"m4","L2":"m2","L3":"m3","L0":"m0","R4":"m1","R1":"m4","R2":"m2","R3":"m3","R0":"m0"},"button":{"PS":"lm1","Options":"X","L1":"e12","R1":"e22"}}
    def on_playstation_button_press(self): self.manage_keys("PS",1)
    def on_playstation_button_release(self): self.manage_keys("PS",0)
    def on_share_press(self): self.manage_keys("Share",1)
    def on_share_release(self): self.manage_keys("Share",0)
    def on_options_press(self): self.manage_keys("Options",1)
    def on_options_release(self): self.manage_keys("Options",0)
    def on_x_press(self): self.manage_keys("X",1)
    def on_x_release(self): self.manage_keys("X",0)
    def on_square_press(self): self.manage_keys("Square",1)
    def on_square_release(self): self.manage_keys("Square",0)
    def on_circle_press(self): self.manage_keys("Circle",1)
    def on_circle_release(self): self.manage_keys("Circle",0)
    def on_triangle_press(self): self.manage_keys("Triangle",1)
    def on_triangle_release(self): self.manage_keys("Triangle",0)
    def on_R1_press(self): self.manage_keys("R1",1)
    def on_R1_release(self): self.manage_keys("R1",0)
    def on_R2_press(self,val=0): self.manage_keys("R2",1)
    def on_R2_release(self): self.manage_keys("R2",0)
    def on_R3_press(self): self.manage_keys("R3",1)
    def on_R3_release(self): self.manage_keys("R3",0)
    def on_L1_press(self): self.manage_keys("L1",1)
    def on_L1_release(self): self.manage_keys("L1",0)
    def on_L2_press(self,val=0): self.manage_keys("L2",1)
    def on_L2_release(self): self.manage_keys("L2",0)
    def on_L3_press(self): self.manage_keys("L3",1)
    def on_L3_release(self): self.manage_keys("L3",0)
    def on_left_arrow_press(self): self.manage_keys("Left",1)
    def on_right_arrow_press(self): self.manage_keys("Right",1)
    def on_down_arrow_press(self): self.manage_keys("Down",1)
    def on_up_arrow_press(self): self.manage_keys("Up",1)
    def on_left_right_arrow_release(self): self.manage_keys("LR",0)
    def on_up_down_arrow_release(self): self.manage_keys("UD",0)
    def on_R3_up(self,val=0): self.manage_keys("R3y",1,val)
    def on_R3_down(self,val=0): self.manage_keys("R3y",1,val)
    def on_R3_left(self,val=0): self.manage_keys("R3x",1,val)
    def on_R3_right(self,val=0): self.manage_keys("R3x",1,val)
    def on_R3_x_at_rest(self,val=0): self.manage_keys("R3x",0,val)
    def on_R3_y_at_rest(self,val=0): self.manage_keys("R3y",9,val)
    def on_L3_up(self,val=0): self.manage_keys("L3y",1,val)
    def on_L3_down(self,val=0): self.manage_keys("L3y",1,val)
    def on_L3_left(self,val=0): self.manage_keys("L3x",1,val)
    def on_L3_right(self,val=0): self.manage_keys("L3x",1,val)
    def on_L3_x_at_rest(self,val=0): self.manage_keys("L3x",0,val)
    def on_L3_y_at_rest(self,val=0): self.manage_keys("L3y",9,val)

    def manage_keys(self,key,value1=0,value2=0):
        if key == "PS":
            os.system("sudo bluetoothctl disconnect {}  > /dev/null".format(self.ip))
        elif key != "L3x" and key != "L3y" and key != "R3x" and key != "R3y":
            if value1: 
                try: self.func(self.process["button"][key])
                except: pass
            else: pass
        else:
            i=0
            last = self.joystick[i]
            if   key == "LR"[i]+"3x" and value2 > 3000: self.joystick[i] = 1
            elif key == "LR"[i]+"3y" and value2 > 3000: self.joystick[i] = 2
            elif key == "LR"[i]+"3x" and value2 < -3000: self.joystick[i] = 3
            elif key == "LR"[i]+"3y" and value2 < -3000: self.joystick[i] = 4
            else: self.joystick[i] = 0
            if last != self.joystick[i]: self.func(self.process["joystick"]["LR"[i]+str(self.joystick[i])])
            if key[0] == "R":
                if key[2] == "x":
                    self.func("s1"+str(int(value2/20000*90+90)))
                if key[2] == "y":
                    self.func("s0"+str(int(-value2/20000*90+90)))



class PS4(Runner):
    def __init__(self,func):
        super(PS4,self).__init__([func])
        self.connected = Variable(None)
    def init(self,func):
        self.func = func
        self.screen = None
        self.ip = IP["ps4"]
        self.controller = MyController(func, interface="/dev/input/js0", connecting_using_ds4drv=False,ip = self.ip)
        Run(self.connect)
    def link(self,screen): self.screen = screen
    def connect(self):
        while True:
            th = Thread(lambda:self.controller.listen(timeout=60,var=self.connected))
            th.start()
            while self.controller.is_connected == False: 
                time.sleep(5)
                os.system("sudo bluetoothctl connect {}  > /dev/null".format(self.ip))

            print(Fore.BLUE+" RPI4: "+Fore.WHITE+f"PS4 Controller connected")
            if self.screen is not None: self.screen.show(self.screen.letters[self.screen.letter_index.index("$")].paint(Color(0,200,100)))
            while self.controller.is_connected: time.sleep(0.1)
            print(Fore.BLUE+" RPI4: "+Fore.WHITE+"PS4 Controller disconnected")
            if self.screen is not None: self.screen.show(self.screen.letters[self.screen.letter_index.index("$")].paint(Color(200,0,100)))
            th.stop()
