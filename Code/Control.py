from Robot import Robot,coords,t
from Thread import Thread,Variable,Runner
from rpi_ws281x import Color
from BT import Arm
import time
from pydub import AudioSegment
import numpy as np
import random
from colorama import Fore

robot = Robot()
arduino_arm = Arm() # Bluetooth connected arm
screen = None
servo = None
wheels = None
ultrasonic = None
camera = None
arm = None

class Controller(Runner): # ROBOT MODES
    def __init__(self,color):
        super(Controller,self).__init__([color])
    def init(self,color):
        self.robot = robot
        self.thread = Thread(self.pause)
        self.mode = [self.pause,self.test,self.get,self.obstacle_avoid,self.say_hi,self.route] # List of modes
        self.loop = [False,False,False,True,False,False,False]
        self.active = 0
        self.tool = 0
        self.color = color
        self.last_route = 0
        self.musicThread=None
        self.musicBar = 0
        global screen,servo,wheels,ultrasonic,camera,arm
        robot.wait()
        screen = robot.screen
        servo = robot.servo
        wheels = robot.wheels
        ultrasonic = robot.head.ultrasonic
        camera = robot.head.camera
        arm = robot.arm1
    def voice(self,v): self.voice = v # link a voice assistant
    def start(self,mode): # start running a mode
        mode += 1
        self.active = mode
        wheels.stop(color=self.color.read())
        screen.animThread.pause()
        self.thread.pause()
        try:
            if mode >= 5: 
                self.thread = Thread(self.route,loop=None,param=(mode-5))
                self.thread.start()
            else:
                self.thread = Thread(self.mode[mode],loop=self.loop[mode])
                self.thread.start()
        except: print("ERROR")
    def pause(self): pass
    def obstacle_avoid(self): # MODE 3
        if ultrasonic.read(2,1) <= 30:
            wheels.stop(color=self.color.read())
            self.tool = 0
            servo.angle(1,180)
            time.sleep(1)
            d1 = ultrasonic.read()
            servo.angle(1,0)
            time.sleep(1)
            d2 = ultrasonic.read()
            servo.angle(1,90)
            if d1 > d2 and d1 > 30: wheels.left(90,1,color=self.color.read())
            if d1 < d2 and d2 > 30: wheels.right(90,1,color=self.color.read())
            if d1 < 20 and d2 < 30: wheels.left(180,1,color=self.color.read())
            time.sleep(1)
        else:
            if self.tool == 0: wheels.front(0,0,color=self.color.read(),speed=1.8)
            self.tool = 1
    def say_hi(self): # MODE 4: Search for a user and say hi to the person (name)
        #robot.animations.hide_arms()
        a = 0
        servo.angle(0,120)
        robot.animations.light_on()
        while camera.coord(camera.read(),0) == (0,0):
            wheels.right(10,1,color=self.color.read(),p=0)
            time.sleep(1)
            a += 10
        time.sleep(1)
        p = robot.head.locate()
        n = None
        while n == None: n = camera.coord(camera.read(),0,rec=1,face_recognizer=camera.face_recognizer)[1]
        screen.text("Hola "+n)
        robot.animations.hi()
        robot.animations.light_off()
    def go_home(self): # Go to coord (0,0,0)
        p = robot.coord.mid.copy()
        p.change((0,0,p.z))
        a = robot.coord.mid_e.a.value()
        b = t.triangle(robot.coord.mid.x,robot.coord.mid.y,-181,-182,-181,90)
        if a <= 0: wheels.right(180+a+b,1,color=self.color.read())
        else: wheels.left(180-a+b,1,color=self.color.read())
        wheels.front(coords.Distance(robot.coord.mid_e.A,p)/10,1,color=self.color.read())
        a = robot.coord.mid_e.a.value()
        if a >= 0: wheels.right(a,1,color=self.color.read())
        else: wheels.left(-a,1,color=self.color.read())
    def go_to(self,q): # Go to coord q
        p = robot.coord.mid.copy()
        p.change((0,0,p.z))
        d=coords.Distance(robot.coord.mid_e.A,q)
        if d>0:
            a = robot.coord.mid_e.a.value()
            b = t.triangle(robot.coord.mid.x-q.x,robot.coord.mid.y-q.y,-181,-182,-181,90)
            if a < 0: a += 360
            if robot.coord.mid.x-q.x > 0: b = -b
            b = 180-a-b
            while b > 360: b -= 360
            while b < 0: b += 360
            if b > 180: wheels.right(360-b,1,color=self.color.read())
            else: wheels.left(b,1,color=self.color.read())
            wheels.front(d/10,1,color=self.color.read())
    def route(self,r): # MODE 5: Follow route r to arrive to a point
        if r != self.last_route:
            if coords.Distance(robot.coord.mid_e.A,robot.coord.home) > 10: self.route_home()
            if r != 0:
                last = robot.coord.path[r-1][len(robot.coord.path[r])-1]
                for point in robot.coord.path[r-1]:
                    if point != last: self.go_to(point)
                    else: self.home()
                    print(robot.coord.mid_e.A.p,robot.coord.mid_e.a.value())
                robot.coord.mid_e.move((last.x-robot.coord.mid_e.A.x,last.y-robot.coord.mid_e.A.y,0))
            self.last_route = r
        elif r != 0: self.go_to(robot.coord.path[r-1][len(robot.coord.path[r])-1])
        else: self.go_home()
        print(robot.coord.mid_e.A.p,robot.coord.mid_e.a.value())
    def route_home(self): # Go home following the routes. (All the routes are connected to home)
        r = self.last_route-1
        if r >= 0:
            for i in range(len(robot.coord.path[r])):
                self.go_to(robot.coord.path[r][len(robot.coord.path[r])-i-1])
        self.go_home()
    def home(self): # Recalculate home (indicated by a green spot on the floor)
        robot.animations.hide_arms()
        while camera.coord(camera.read(),1,mask=camera.green_mask) == (0,0):
            wheels.right(10,1,color=self.color.read(),p=0)
            time.sleep(1)
        b = robot.coord.mid_e.a.value()
        robot.coord.mid_e.rotate(-b)
        p = robot.head.locate(1,0,1,down=0)
        p.move((0,0,127-p.z))
        
        p2 = p.copy()

        a = t.triangle(p2.x,p2.y,-181,-182,-181,90)
        if p2.x >= 0: wheels.left(a,1,color=self.color.read())
        else: wheels.right(a,1,color=self.color.read())

        f = coords.Distance(robot.coord.mid,p)/10-15
        wheels.front(f,1,color=self.color.read())
        robot.coord.mid_e.rotate(b)
    
    def get(self): # MODE 2: Grab a green item
        servo.angle(1,70)
        robot.animations.hide_arms()
        while camera.coord(camera.read(),1,mask=camera.green_mask) == (0,0):
            wheels.right(10)
            time.sleep(1)
        
        b = robot.coord.mid_e.a.value()
        robot.coord.mid_e.rotate(-b)
        p = robot.head.locate(1,0,1,down=1)
        p.move((0,0,127-p.z))
        
        p2 = p.copy()

        a = t.triangle(p2.x,p2.y,-181,-182,-181,90)
        robot.animations.sleep2()
        if p2.x >= 0: wheels.left(a)
        else: wheels.right(a)

        f = coords.Distance(robot.coord.mid,p)/10-15
        wheels.front(f)
        arm.hand(arm.OPEN)
        robot.coord.mid_e.rotate(20)
        arm.move(p)
        robot.coord.mid_e.rotate(-20)
        time.sleep(.5)
        wheels.left(25)
        arm.hand(arm.CLOSE)
        time.sleep(.5)
        wheels.right(25)
        wheels.back(f)
        if p2.x >= 0: wheels.right(a)
        else: wheels.left(a)
        robot.coord.mid_e.rotate(b)
        arm.hand(arm.OPEN)
    def present(self): # Robot presents itself (in spanish)
        self.voice.say("Hola, este es el producto final")
        self.voice.say("Déjame presentarte mis nuevas funciones: ahora puedo hablar contigo mediante una inteligencia artificial y puedes jugar a minijuegos en mi screen. Además, puedo controlar enchufes inteligentes.")
        self.voice.say("Tengo una pantalla led RGB")
        self.voice.say("Mi cabeza, tiene dos ejes para el cuello y en ella está mi cámara y un sensor de ultrasonidos para distancias.")
        robot.animations.hi(1)
        time.sleep(.1)
        screen.text("r",fg=Color(150,0,0),bg=Color(1,1,1))
        time.sleep(.1)
        screen.text("g",fg=Color(0,150,0),bg=Color(1,1,1))
        time.sleep(.1)
        screen.text("b ",fg=Color(0,0,150),bg=Color(1,1,1))
        screen.text("$ ",fg=Color(0,100,200),bg=Color(0,1,0))
        servo.angle(1,120)
        servo.angle(0,120)
        time.sleep(.5)
        servo.angle(1,60)
        time.sleep(.5)
        robot.animations.sleep()
        self.voice.say("Con mis brazos, puedo coger cualquier objeto en un espacio amplio.")
        self.voice.say("Además, puedo moverme de manera precisa gracias a mis ruedas.")
        robot.servo.angle(2,180)
        robot.servo.angle(3,0)
        robot.servo.angle(4,0)
        robot.servo.angle(5,180)
        robot.servo.angle(6,0)
        robot.servo.angle(7,180)
        robot.servo.angle(8,180)
        robot.servo.angle(9,0)
        time.sleep(1)
        robot.animations.sleep()
        robot.wheels.front(20)
        robot.wheels.back(20)
        robot.wheels.right(20)
        robot.wheels.left(20)
        ###
        self.voice.say("Otra de mis funciones es enviar correos, acabo de enviarte uno.")
        self.voice.say("También puedo entenderte si me hablas.")
        robot.mail.send(to=robot.mail.mailCarlos,subject="Correo",body="Hola!!!, este mensaje de correo se ha enviado desde el robot a traves de Python utilizando la libreria SMPT. Esta herramienta puede ayudar bastante a los pacientes con enfermedades neuromusculares que necesiten enviar correos rapidamente.")
        self.voice.say("Para controlarme, puedes hablarme o puedes conectarte desde mi aplicación a un servidor para enviarme órdenes.")
        self.voice.say("Además, el desarrollo de este proyecto, así como información acerca de las enfermedades neuromusculares se encuentra en la página web. https://carlocaal.eu.pythonanywhere.com")
        ###
    def dance(self,song,func): # Dance, play music and show a sound animation on the screen
        robot.screen.wait_()
        robot.screen.toogleRainbow(2,4)
        t = .1
        sound = AudioSegment.from_file(song+'.mp3')
        raw_data = sound.raw_data
        amplitudes = np.fromstring(raw_data, dtype=np.int16)
        sample_rate = sound.frame_rate
        intensities = []
        for i in range(0, len(amplitudes), int(sample_rate*t)):
            chunk = amplitudes[i:i+int(sample_rate*t)]
            intensity = np.mean(np.abs(chunk))
            intensities.append(intensity)
        func(song,1)
        self.musicBar = time.time()
        max = sound.max
        min = 600
        self.musicThread = Thread(func=self.soundbars,param=(max,min,intensities,t/2),loop=True)
        self.danceThread = Thread(func=self.dance_animations,loop=True)
        self.musicThread.start()
        self.danceThread.start()
    def dance_animations(self): random.choice(robot.animations.dances)()
    def soundbars(self,max,min,intensities,t):
        try:
            intensity = intensities[int((time.time()-self.musicBar)/t)]
            i = 0
            if intensity > max/2.5: i=8
            elif intensity < min: i=0
            else: i = int(6*(intensity-min)/(max/2.5-min)+1)
            robot.screen.soundbar(i)
            if (time.time()-self.musicBar)/t >= len(intensities): self.stopMusic()
            time.sleep(t)
        except: pass
    def stopMusic(self):
        if self.musicThread is not None: self.musicThread.pause()
        if self.danceThread is not None: self.danceThread.pause()
        robot.screen.toogleRainbow(1,1)
    def maze(self): # Escape from a maze
        if robot.head.read(robot.head.LEFT) > 20: 
            robot.wheels.left(90)
            robot.wheels.front(20)
        elif robot.head.read(robot.head.FRONT) > 20: 
            robot.wheels.front(20)
        elif robot.head.read(robot.head.RIGHT) > 20: 
            robot.wheels.right(90)
        else: 
            robot.wheels.left(180)
            robot.wheels.front(20)
    def test(self): # MODE 1: Send data to arduino arm (still provisional)
        if not arduino_arm.started: print(Fore.MAGENTA+"ERROR:"+Fore.WHHITE+" Robotic arm disconnected")
        else:
            arduino_arm.grab([-20, 170, 10])
            time.sleep(1)
            arduino_arm.release([110, 20, 40])
            time.sleep(1)
            servo.angle(5,180)
            arduino_arm.sleep()

if __name__ == "__main__":
    control = Controller(Variable(Color(0,100,200)))
    input()
    robot.head.locate(1,1,1,down=1)