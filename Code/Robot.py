from Camera import Camera
from Motor import Motor
from Screen import Screen
from Servo import Servo
from Ultrasonic import Ultrasonic
from Mail import Mail
from Math import t,Coords
from Thread import Runner

from rpi_ws281x import Color
import time
import cv2 as cv
import numpy as np

import RPi.GPIO as Pin
Pin.setwarnings(False)
Pin.setmode(Pin.BCM)
coords = Coords()

class Robot(Runner):
    def __init__(self):
        super(Robot,self).__init__(None)
    def init(self):
        self.mail = Mail()
        self.screen = Screen()
        self.servo = Servo()
        self.coord = self.Coord(self.servo)
        self.head = self.Head(Pin,self.servo,[0,1],self.coord)
        self.wheels = self.Wheels(Pin,self.screen,self.coord)
        self.arm1 = self.Arm(-1,self.servo,[2,3,4,5],self.coord,[self.coord.arm1a,self.coord.arm2a,self.coord.arm3a,self.coord.arm4a])
        self.arm2 = self.Arm(1,self.servo,[6,7,8,9],self.coord,[self.coord.arm1b,self.coord.arm2b,self.coord.arm3b,self.coord.arm4b])
        self.animations = self.Animations(self.screen,self.servo,self.wheels)
    def catch(self,p,i=0): # Function to grab an object (small Distance)
        if coords.Distance(p,self.coord.arm1a.A) < coords.Distance(p,self.coord.arm1b.A): self.arm1.get(p,i)
        else: self.arm2.get(p,i)
  
    class Coord: # Coordinates of all the robot parts
        def __init__(self,srv):
            self.home = coords.Point((0,0,15))
            self.servo = srv
            self.bottom = coords.Figure([coords.Point((60,65,15)),coords.Point((-60,65,15)),coords.Point((-60,-55,15)),coords.Point((60,-55,15))])
            self.top = coords.Figure([coords.Point((60,65,137)),coords.Point((-60,65,137)),coords.Point((-60,-55,137)),coords.Point((60,-55,137))])
            self.left = coords.Figure([coords.Point((60,-55,15)),coords.Point((-60,-55,15)),coords.Point((-60,-55,137)),coords.Point((60,-55,137))])
            self.right = coords.Figure([coords.Point((-60,65,15)),coords.Point((60,65,15)),coords.Point((60,65,137)),coords.Point((-60,65,137))])
            self.cam = coords.Point((0,97,154))
            self.ultrasonic = coords.Point((0,105,187))
            self.neck2 = coords.Vector((coords.Point((-10,63,188)),coords.Point((-30,63,188))))
            self.neck1 = coords.Vector((coords.Point((-5,55,147)),coords.Point((-5,55,167))))
            #self.target = coords.Point((60,120,117)) # Example point
            self.arm4a = coords.Point((-85,155,127))
            self.arm4b = coords.Point((85,155,127))
            self.path = [[coords.Point((1000,1000,15)),coords.Point((2000,1000,15)),coords.Point((2100,1000,15)),coords.Point((3000,1000,15))],[coords.Point((1000,1000,15)),coords.Point((1000,2000,15)),coords.Point((2000,2000,15)),coords.Point((3000,2000,15))],[coords.Point((1000,1000,15)),coords.Point((1000,2000,15)),coords.Point((2000,2000,15)),coords.Point((3000,2000,15))],[coords.Point((1000,1000,15)),coords.Point((1000,2000,15)),coords.Point((2000,2000,15)),coords.Point((3000,2000,15))]]
            self.arm3a = coords.Vector((coords.Point((-85,92,137)),coords.Point((-85,92,117))))
            self.arm3b = coords.Vector((coords.Point((85,92,137)),coords.Point((85,92,117))))
            self.arm2a = coords.Vector((coords.Point((-85,50,137)),coords.Point((-85,50,117))))
            self.arm2b = coords.Vector((coords.Point((85,50,137)),coords.Point((85,50,117))))
            self.arm1a = coords.Vector((coords.Point((-55,45,116)),coords.Point((-75,45,116))))
            self.arm1b = coords.Vector((coords.Point((55,45,116)),coords.Point((75,45,116))))
            self.mid = coords.Point((0,0,15),[self.bottom,self.top,self.left,self.right,self.neck1,self.neck2,self.cam,self.ultrasonic,self.arm1a,self.arm1b,self.arm2a,self.arm2b,self.arm3a,self.arm3b,self.arm4a,self.arm4b])
            self.mid_e = coords.Vector((self.mid,coords.Point((0,0,0))))

        def rotate(self,motor,vector,angle,item,f,angle2=None,retry=0): # rotate a servo both physically and mathematically
            d = self.mid_e.a.value()
            self.mid_e.rotate(-d)
            if f != 0:
                for i in item: vector.rotate(-vector.a.value(),i)
                vector.rotate(-vector.a.value())
                for i in item: vector.rotate(f*(angle-90),i)
                vector.rotate(f*(angle-90))
            if angle2 is None: angle2 = angle
            self.servo.angle(motor,angle2)
            self.mid_e.rotate(d)

    class Arm:
        def __init__(self,s,srv,i,c,p):
            self.servo = srv
            self.s,self.i,self.p,self.c = s,i,p,c
            self.OPEN,self.CLOSE = 0,1
        def hand(self,state,retry=0): self.c.rotate(self.i[3],0,90*(-2*state*(self.s-1)/2+1-state),[],0,retry=retry)
        def move(self,p,i=0): # move arm to a point
            d = self.c.mid_e.a.value()
            self.c.mid_e.rotate(-d)
            p = p.copy()
            copy = self.p
            self.p = [copy[0].copy(),copy[1].copy(),copy[2].copy(),copy[3].copy()]
            if p.z == 127: p.z = 126.999
            if coords.Distance(p,self.p[1].A) < 200:
                P = coords.Plane(self.p[0])
                v,A,B = P.adapt(self.p[0].A),P.adapt(self.p[3]),P.adapt(p)
                v.z,A.z,B.z = 0,0,0
                a = t.triangle(coords.Distance(A,B),coords.Distance(A,v),coords.Distance(v,B),-182,-181,-181)
                if p.z > self.p[3].z: a = -a
                self.c.rotate(self.i[0],self.p[0],-a+90,self.p[1:],self.s,90+a)
                P = coords.Plane(self.p[1])
                v,u,A,B = P.adapt(self.p[1].A),P.adapt(self.p[2].A),P.adapt(self.p[3]),P.adapt(p)
                c = -(180 - t.triangle(coords.Distance(v,B),coords.Distance(u,v),coords.Distance(u,A),-182,-181,-181))
                self.c.rotate(self.i[2],self.p[2],90+c,self.p[3:],self.s,90-self.s*c)
                P = coords.Plane(self.p[1])
                v,u,A,B = P.adapt(self.p[1].A),P.adapt(self.p[2].A),P.adapt(self.p[3]),P.adapt(p)
                b = t.triangle(coords.Distance(A,B),coords.Distance(B,v),coords.Distance(v,A),-182,-181,-181)
                self.c.rotate(self.i[1],self.p[1],90+b,self.p[2:],self.s,90+self.s*b)
            else: print("ERROR")
            self.p = copy
            self.c.mid_e.rotate(d)
        def get(self,p,i=0): # grab an object
            self.hand(self.OPEN)
            time.sleep(1)
            self.move(p,i)
            time.sleep(1)
            self.hand(self.CLOSE,retry=1)
    class Head:
        def __init__(self,Pin,srv,pin,coord):
            self.ultrasonic = Ultrasonic(Pin,14,15)
            self.camera = Camera()
            self.pin,self.servo = pin,srv
            self.c = coord
            self.LEFT,self.FRONT,self.RIGHT = 180,90,0
        def coord(self,h=0): # Calculate the coords of the object the robot is looking at
            d = 10000
            while d >= 1000: d=self.ultrasonic.read()*10
            b,a = self.servo.mem[0],self.servo.mem[1]-90+self.c.mid_e.a.value()
            d2 = t.triangle(d,-182,-181,90,-181,a)
            x,y,z = t.triangle(d,-182,-181,90,a,-181),t.triangle(d2,-182,-181,90,b,-181),t.triangle(d2,-182,-181,90,-181,b)
            if a < 90 and a > -90: z *= -1
            p = self.c.ultrasonic
            if h == 1: z = 127
            return coords.Point((-p.x+x,p.y+y,p.z+z))
        def track(self,i,m,img,down=0): # Follow an object with the head
            x,y = self.camera.coord(img,i,mask=[self.camera.green_mask,self.camera.blue_mask,self.camera.yellow_mask][m],down=down)
            if (x,y) != (0,0):
                d = self.c.neck1.a.value()
                self.c.neck1.rotate(-d)
                a = (1-y/240)*39 # Map angle
                if not (y > 230 and y < 250) != 240: self.c.rotate(self.pin[1],self.c.neck2,self.servo.mem[self.pin[1]]+a,[self.c.ultrasonic,self.c.cam],-1)
                self.c.neck1.rotate(d)
                a = (x/320-1)*52
                if not (x > 315 and x < 325): self.c.rotate(self.pin[0],self.c.neck1,self.servo.mem[self.pin[0]]-a,[self.c.ultrasonic,self.c.cam,self.c.neck2],1)
            if x > 315 and x < 325 and y > 230 and y < 250: return 1
            else: return 0
        def locate(self,i=0,m=0,h=0,down=1): # Determine the exact position of an object to identify
            s = 0
            while s != 1:
                img = self.camera.read()
                s = self.track(i,m,img,down=down)

                self.camera.show(img)
                img = 0 * np.ones((400,400,3),dtype = np.uint8)
                coords.Plane(coords.Vector((coords.Point((0,0,15)),coords.Point((0,15,10))))).show(img,self.c.mid_e)
                cv.imshow('IMAGEN',cv.resize(img,(500,500),interpolation= cv.INTER_CUBIC))
                
                if self.camera.stop(): break
            return self.coord(h)
        def panoramic(self): # Make panoramic photographs
            if True:
                time.sleep(1)
                photos = []
                for i in range(3):
                    self.servo.angle(self.pin[0],142-52*i)
                    time.sleep(1)
                    photos.append(self.camera.photo())
                self.servo.angle(self.pin[0],90)
                time.sleep(1)
                return self.camera.panoramic(photos)
        def look_front(self):
            self.c.rotate(self.pin[0],self.c.neck2,[self.c.ultrasonic,self.c.cam],1)
            self.c.rotate(self.pin[1],self.c.neck1,[self.c.ultrasonic,self.c.cam],1)
        def read(self,dir):
            self.servo.set([dir,100,0,0,0,0,0,0,0,0],0)
            time.sleep(.5)
            return self.ultrasonic.read()

    class Wheels: # Coordinates screen and wheels
        def __init__(self,Pin,screen,coord):
            self.motor = Motor(Pin)
            self.screen,self.c = screen,coord
            self.color = Color(100,100,100)
            self.t1 = time.time()
            self.i = 4 # Active movement (default is stop)
        def front(self,l=0,color=None,p=1): self.template(l,color,self.motor.front,0,p)
        def back(self,l=0,color=None,p=1): self.template(l,color,self.motor.back,2,p)
        def left(self,l=0,color=None,p=1): self.template(l,color,self.motor.left,3,p)
        def right(self,l=0,color=None,p=1): self.template(l,color,self.motor.right,1,p)
        def stop(self,color=None,p=1):
            l = 0 # Distance travelled since last call
            t = time.time()-self.t1 # Time difference to calculate Distance travelled
            if self.i == 0: l = self.motor.calc_inv(t,"v1")
            if self.i == 2: l = self.motor.calc_inv(t,"v2")
            if self.i == 1: l = self.motor.calc_inv(t,"w2")
            if self.i == 3: l = self.motor.calc_inv(t,"w1")
            self.calc(l,self.i) # Register previous movement
            self.template(0,color,self.motor.stop,4,p,0)
        def template(self,l,color,func,i,p,o=1): # Template for any movement (save lines)
            if color == None: color = self.color.read() # If no color is given, use robot's current color
            if self.i != 4 and o == 1: self.stop(p=0) # If robot is moving, first, stop robot
            if p: self.screen.anim(self.screen.animation[i].paint(color)) # Start the movement screen animation (if p param)
            func(l) # Move
            if l != 0:
                if o: self.calc(l,i) # Register movement if desired (o param)
                self.motor.stop()
                self.i = 4
                try: self.screen.animThread.pause()
                except: pass
            else: # If no Distance is given, record the time
                self.t1 = time.time()
                self.i = i
        def calc(self,l,i): # Register movement geometrically
            if i == 1 or i == 3:
                self.c.mid_e.rotate((i-2)*l)
            if i == 0 or i == 2:
                l = l*10 # CM to MM
                a = self.c.mid_e.a.value()
                d = -l*(i-1)
                if a == 0: y,x = d,0
                else: y,x = t.triangle(d, -182, -181, 90, -181, a), t.triangle(d, -182, -181, 90, a, -181)
                self.c.mid_e.move((x,y,0))

    class Animations: # Several animations
        def __init__(self,screen,servo,wheels):
            self.screen = screen
            self.servo = servo
            self.wheels = wheels
            self.animations = [self.dance1,self.hi,self.hide_arms,self.sleep]
            self.dances = [self.dance1,self.dance2,self.dance3,self.dance4,self.dance5,self.dance6,self.dance7,self.dance8]
        def sleep(self): self.servo.simetric_move([90,90,90,90,90,90],.5)
        def sleep2(self): self.servo.set([90,90,90,90,90,90,None,None,None,None],0)
        def light_on(self): self.screen.text("#",fg=Color(255,255,255))
        def light_off(self): self.screen.text("#",fg=Color(0,0,1),bg=Color(255,255,255))
        def dance0(self):
            mem = []
            for i in self.servo.mem: mem.append(i)
            self.screen.show(self.screen.letters[self.screen.letter_index.index("&")].paint(Color(0,0,0)))
            self.servo.angle(3,0)
            self.servo.angle(7,180)
            for i in range(4):
                for i in range(2):
                    self.servo.angle(2,i*180)
                    self.servo.angle(6,i*180)
                    time.sleep(1)
            for i in range(10): self.servo.angle(i,mem[i])
        def hi(self,n=3):
            mem = []
            for i in self.servo.mem: mem.append(i)
            self.screen.show(self.screen.letters[self.screen.letter_index.index("&")].paint(Color(0,0,0)))
            self.servo.angle(2,180)
            self.servo.angle(3,45)
            self.servo.angle(5,135)
            for j in range(n):
                for i in range(2):
                    self.servo.angle(4,i*90+1)
                    time.sleep(1)
            for i in range(10): self.servo.angle(i,mem[i])
        def hide_arms(self): self.servo.set([None,None,30,0,0,180,150,180,180,0],1)
        def dance0b(self): 
            self.servo.simetric_move([120,80,180,0,0,180],2)
            self.sleep()
        def dance7(self): 
            self.servo.simetric_move([90,90,90,90,0,180],1)
            self.servo.simetric_move([120,90,110,90,0,180],.5)
            self.servo.simetric_move([90,90,90,90,0,180],.5)
            self.sleep()
        def dance2(self): 
            self.servo.simetric_move([90,90,180,45,90,90],1)
            self.sleep()
        def dance3(self): 
            self.servo.simetric_move([90,90,180,90,90,90],.5)
            for i in range(3):
                self.servo.move([90,90,180,30,90,90,0,60,90,90],.5)
                self.servo.move([90,90,180,120,90,90,0,150,90,90],.5)
            self.servo.simetric_move([90,90,180,90,90,90],.5)
            self.sleep()
        def dance4(self): 
            for i in range(3):
                self.servo.move([90,90,150,90,90,90,150,90,90,90],.5)
                self.servo.move([90,90,30,90,90,90,30,90,90,90],.5)
            self.sleep()
        def dance5(self): 
            for i in range(3):
                self.servo.simetric_move([90,90,120,90,90,90],.2)
                self.servo.simetric_move([90,90,90,30,60,90],.2)
                self.servo.simetric_move([90,90,60,90,90,90],.2)
                self.servo.simetric_move([90,90,90,90,60,90],.2)
            self.sleep()
        def dance6(self): 
            for i in range(3):
                self.servo.simetric_move([70,90,180,0,0,90],.4)
                self.servo.simetric_move([110,90,180,100,80,90],.4)
            self.servo.simetric_move([90,90,180,0,0,90],.4)
            self.sleep()
        def dance1(self): 
            for i in range(3):
                self.servo.move([90,90,0,0,90,90,0,180,90,90],.5)
                self.servo.move([90,90,180,0,90,90,180,180,90,90],.5)
                self.sleep()
        def dance8(self): 
            for i in range(3):
                self.servo.simetric_move([90,90,180,0,90,90],.5)
                self.servo.simetric_move([90,90,0,0,90,90],.5)
                self.sleep()

