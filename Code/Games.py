from Screen import Color,Screen
from Thread import Thread,Variable, Run

import time
import random

from pynput import keyboard as kb
from Thread import Runner

class Keyboard(Runner):
    def __init__(self):
        super(Keyboard,self).__init__(None)
    def init(self):
        self.key = [0,0,0,0,0]
        self.last,self.active = self.matrix(),0
        self.listener = kb.Listener(self.press,self.release)
        self.listener.start()
    def matrix(self): return 8*self.key[0] + 4*self.key[1] + 2*self.key[2] +self.key[3]
    def press(self,key): self.template(str(key),1)
    def release(self,key): self.template(str(key),0)
    def template(self,key,t):
        for i in range(5):
            if key == ["Key.up","Key.down","Key.left","Key.right","Key.enter"][i]: self.key[i],self.active = t,i+1
        if self.matrix() != self.last: self.last = self.matrix()

class Nothing:
    def __init__(self): pass
    def soundEffect(self,msg):pass
keyboard = Keyboard()
screen = Variable(None)
assistant = Variable(None)
assistant.write(Nothing())

def lichess_start():
    global lichess_game
    from API import lichess_game as lg
    lichess_game = lg
Run(lichess_start) # Save time

class Pixel:
    def __init__(self,p,c,limits=(-2,-1,100,20),teleport=0):
        self.x = p[0]
        self.y = p[1]
        self.c = c
        self.boss = None
        self.mx = 0
        self.my = 0
        self.clock = 0
        self.kb = None
        self.limit = limits
        self.teleport = teleport
    def move(self,x,y,save=1):
        x2,y2 = self.x + x,self.y + y
        if self.teleport == 0:
            if x2 > self.limit[2]: x2 = self.limit[2]
            if x2 < self.limit[0]: x2 = self.limit[0]
            if y2 > self.limit[3]: y2 = self.limit[3]
            if y2 < self.limit[1]: y2 = self.limit[1]
        else:
            if x2 > self.limit[2]: x2 = self.limit[0]
            if x2 < self.limit[0]: x2 = self.limit[2]
            if y2 > self.limit[3]: y2 = self.limit[1]
            if y2 < self.limit[1]: y2 = self.limit[3]
        if self.boss is not None: self.boss.move((self.x,self.y),(x2,y2),save=save)
        self.x,self.y = x2,y2
    def makeMoveable(self,x,y,clock,kb):
        self.clock = clock
        self.mx = x
        self.my = y
        self.kb = kb
        self.moveThread = Thread(self.update,loop=True)
        self.moveThread.start()
    def update(self):
        c = (self.x,self.y)
        self.boss.screen.pixel(c,self.c,save=False,show=True)
        time.sleep(self.clock)
        if self.mx == 1:
            self.move(self.kb.key[3],0,save=0)
            self.move(-self.kb.key[2],0,save=0)
        if self.my == 1:
            self.move(0,self.kb.key[1],save=0)
            self.move(0,-self.kb.key[0],save=0)
        self.boss.screen.pixel(c,Color(0,0,1),save=False,show=True)
    def show(self):
        if self.boss.pixelOn((self.x,self.y),color=self.c,color3=Color(2,2,2))==0 and self.boss.pixelOn((self.x,self.y),color=self.c)==1: pass
        else: self.boss.screen.pixel((self.x,self.y),self.c,save=False,show=True)
    def kill(self):
        try: self.moveThread.pause()
        except: pass
        if self in self.boss.pixels: self.boss.pixels.remove(self)
        self.boss.screen.pixel((self.x,self.y),Color(0,0,1),save=False,show=True)
    def fill(self,color): self.c = color

class Object:
    def __init__(self,p,t=0,nu=(0,0),func=None,func2=None):
        self.pixels = p
        self.l = 1
        self.mx = 0
        self.my = 0
        self.clock = 0
        self.kb = None
        self.nu = nu
        self.func = func
        self.func2 = func2
        self.c = p[0].c
        self.type = t
        self.paintC = Color(0,255,0)
    def makeMoveable(self,x,y,clock,kb,color2=Color(0,0,0),t=0):
        self.clock = clock
        self.mx = x
        self.my = y
        self.kb = kb
        self.t = t
        self.p = 0
        self.h = 0
        self.u = 0
        self.time = 1
        self.moveThread = Thread(self.update,loop=True)
        if self.t == 0: self.moveThread.start()
        self.color2 = color2
    def update(self):
        c = []
        for i in self.pixels:
            i.boss.screen.pixel((i.x,i.y),i.c,save=False,show=False)
            c.append([i.x,i.y])
        if self.t == 0 or self.type == 3:
            self.pixels[0].boss.screen.strip.show()
            time.sleep(self.clock)
            self.pixels[0].boss.screen.strip.show()
            if self.mx == 1:
                self.move(self.kb.key[3],0,save=0)
                self.move(-self.kb.key[2],0,save=0)
            if self.my == 1:
                self.move(0,self.kb.key[1],save=0)
                self.move(0,-self.kb.key[0],save=0)
            self.pixels[0].boss.move((-10,-10),(-10,-11))
            for j in range(len(self.pixels)):
                i = self.pixels[j]
                i.boss.screen.pixel(c[j],Color(0,0,1),save=False,show=False)
            if self.type == 1: self.check()
        elif self.t == 1:
            if self.kb.key[0] and self.u == 0 or self.kb.key[0] and self.p > 2 and self.u !=2 or self.kb.key[0] and self.p<0 and self.u !=2:
                assistant.read().soundEffect('bip')
                self.u += 1
                if self.p <1 or self.p == 11: self.p = 2
                else: self.p += 2
            if self.p == 1:
                self.move(0,-1,save=1)
                self.h += 1
                self.p = 10
            if self.p > 1 and self.p < 10:
                self.move(0,-1,save=1)
                self.h += 1
                self.p -= 1
            if self.pixels[0].boss.pixelOn((self.pixels[0].x,self.pixels[0].y+1),color=Color(255,0,0)):
                self.p = 0
                self.u = 0
            if self.p < 0:
                self.move(0,1,save=1)
                if self.kb.key[1] and self.time == 1: 
                    self.h -= 1
                    self.p += 1
                    self.time = 0
                else: self.time = 1
            if self.h == 0 and self.pixels[0].boss.pixelOn((self.pixels[0].x,self.pixels[0].y+1),color=Color(255,0,0)): self.u = 0
            if self.h == 0 and self.pixels[0].boss.pixelOn((self.pixels[0].x,self.pixels[0].y+1),color=Color(255,0,0)) == False and self.pixels[0].boss.pixelOn((self.pixels[0].x,self.pixels[0].y+1),color=Color(9,0,0)) == True: self.p = -10
            if self.p == 11: self.p = -self.h
            if self.p == 10 or self.pixels[0].boss.pixelOn((self.pixels[0].x,self.pixels[0].y+1),color=Color(255,0,0)) and self.h > 0 and self.p < 1: 
                self.p = 11
            for j in range(len(self.pixels)):
                i = self.pixels[j]
                i.boss.screen.pixel(c[j],Color(0,0,1),save=False,show=False)
            self.check()
            self.pixels[0].boss.move((-10,-10),(-10,-11))
        elif self.t == 2:
            self.move(-1,0,save=0)
            self.pixels[0].boss.move((-10,-10),(-10,-11))
            for j in range(len(self.pixels)):
                i = self.pixels[j]
                i.boss.screen.pixel(c[j],Color(0,0,1),save=False,show=False)
            self.check()

    def move(self,x,y,save=1):
        for i in self.pixels: i.move(x,y,save=save)
    def kill(self):
        try: self.moveThread.pause()
        except: pass
        for i in self.pixels: i.kill()
    def check(self): 
        if self.t == 0 and self.pixels[0].boss.pixelOn((self.pixels[0].x+self.nu[0],self.pixels[0].y+self.nu[1]),color2=self.color2) and self.func is not None and self.kb is not None: 
            self.fill(self.paintC)
            if self.kb.key[4]: self.func((self.pixels[0].x+self.nu[0],self.pixels[0].y+self.nu[1]))
            elif self.func2 != None: self.func2((self.pixels[0].x+self.nu[0],self.pixels[0].y+self.nu[1]))
        elif self.type == 3:
            print("_")
            if self.kb.key[4]: self.func((self.pixels[0].x+self.nu[0],self.pixels[0].y+self.nu[1]))
        elif self.t == 1:
            if self.kb.key[1]: 
                self.func((self.pixels[0].x+self.nu[0],self.pixels[0].y+self.nu[1]))
                self.l = 1
            elif self.func2 != None: 
                self.func2((self.pixels[0].x+self.nu[0],self.pixels[0].y+self.nu[1]))
                self.l = 0
        elif self.t == 2 and self.pixels[0].x == -2: self.func(self)
        elif self.t == 0: self.fill(self.c)
    def fill(self,color):
        for i in self.pixels: i.fill(color)

class Chain:
    def __init__(self,p,t=0,nu=(0,0),func=None,move=0):
        self.pixels = p
        self.mx = 0
        self.my = 0
        self.clock = 0
        self.kb = None
        self.nu = nu
        self.func = func
        self.c = p[0].c
        self.type = t
        self.moveable = move
    def makeMoveable(self,x,y,clock,kb,diagonal=1,paintC=Color(0,255,0)):
        self.clock = clock
        self.mx = x
        self.my = y
        self.kb = kb
        if self.moveable: self.kb.active = 0
        self.d = diagonal
        self.moveThread = Thread(self.update,loop=True)
        self.moveThread.start()
        self.paintC = paintC
    def update(self):
        c = []
        for i in self.pixels:
            i.boss.screen.pixel((i.x,i.y),i.c,save=False,show=False)
            c.append([i.x,i.y])
        self.pixels[0].boss.screen.strip.show()
        time.sleep(self.clock)
        self.pixels[0].boss.screen.strip.show()
        if self.moveable == 0:
            if self.mx == 1 and self.my == 1 and self.d == 1: self.move(self.kb.key[3]-self.kb.key[2],self.kb.key[1]-self.kb.key[0],save=0)
            elif self.mx == 1 and self.kb.key[3]-self.kb.key[2] != 0: self.move(self.kb.key[3]-self.kb.key[2],0,save=0)
            elif self.my == 1: self.move(0,self.kb.key[1]-self.kb.key[0],save=0)
        else: 
            n = self.kb.active
            if n == 1: self.move(0,-1,save=0)
            if n == 2: self.move(0,1,save=0)
            if n == 3: self.move(-1,0,save=0)
            if n == 4: self.move(1,0,save=0)
        self.pixels[0].boss.move((-10,-10),(-10,-11))
        for j in range(len(self.pixels)):
            i = self.pixels[j]
        i.boss.screen.pixel(c[len(c)-1],Color(0,0,1),save=False,show=False)
        if self.type == 1: self.check()
    def move(self,x,y,save=1):
        if x != 0 or y != 0:
            c = (self.pixels[0].x,self.pixels[0].y)
            self.pixels[0].move(x,y,save=0)
            if c != (self.pixels[0].x,self.pixels[0].y):
                self.pixels[0].move(-x,-y,save=0)
                for i in range(len(self.pixels)-1,0,-1):
                    self.pixels[i].move(self.pixels[i-1].x-self.pixels[i].x,self.pixels[i-1].y-self.pixels[i].y,save=0)
                self.pixels[0].move(x,y,save=save)
                if self.type == 2: self.func()
    def kill(self):
        try: self.moveThread.pause()
        except: pass
        for i in self.pixels: i.kill()
    def check(self): 
        if self.pixels[0].boss.pixelOn((self.pixels[0].x+self.nu[0],self.pixels[0].y+self.nu[1])) and self.func is not None and self.kb is not None: 
            self.fill(self.paintC)
            if self.kb.enter: self.func((self.pixels[0].x+self.nu[0],self.pixels[0].y+self.nu[1]))
        else: self.fill(self.c)
    def fill(self,color):
        for i in self.pixels: i.fill(color)

class Field:
    def __init__(self,screen):
        self.screen = screen
        self.pixels = []
    def add(self,pixel): 
        self.pixels.append(pixel)
        pixel.boss = self
    def remove(self,pixel): 
        if pixel in self.pixels: self.pixels.remove(pixel)
    def move(self,p1=(-2,-2),p2=(-2,-3),save=1): 
        if p2 != p1 and save:
            self.screen.pixel(p1,Color(0,0,1),save=False,show=False)
            self.screen.pixel(p2,Color(0,0,1),save=False,show=False)
            for i in self.pixels:
                self.screen.pixel((i.x,i.y),i.c,save=False,show=True)
            self.screen.strip.show()
    def addObj(self,obj):
        for i in obj.pixels: self.add(i)
    def show(self): self.screen.strip.show()
    def pixelOn(self,c,color=(0,0,0),color2=Color(0,0,0),color3=(0,0,0)):
        r = 0
        for pixel in self.pixels:
            if (pixel.x,pixel.y) == c and pixel.c != color and pixel.c != color3: r = 1
            if (pixel.x,pixel.y) == c and pixel.c == color2 and color2 != Color(0,0,0): r = 1
        return r
    def kill(self):
        for i in self.pixels: i.kill()

class Menu:
    def __init__(self):
        screen.read().clean()
        self.field = Field(screen.read())
        p0 = Pixel((6,1),Color(100,100,100),(-1,-1,8,8))
        p1 = Pixel((1,1),Color(0,0,255),(-1,-1,8,8))
        p2 = Pixel((1,3),Color(255,0,0),(-1,-1,8,8))
        p3 = Pixel((1,5),Color(0,255,0),(-1,-1,8,8))
        p4 = Pixel((3,1),Color(120,120,0),(-1,-1,8,8))
        p5 = Pixel((3,3),Color(120,0,120),(-1,-1,8,8))
        self.mouse = Object([Pixel((6,7),6579300,(0,1,7,8)),Pixel((7,6),6579300,(1,0,8,7)),Pixel((6,5),6579300,(0,-1,7,6)),Pixel((5,6),6579300,(-1,0,6,7))],t=1,nu=(0,-1),func=self.notify)
        self.field.add(p0),self.field.add(p1),self.field.add(p2),self.field.add(p3),self.field.add(p4),self.field.add(p5)
        self.field.addObj(self.mouse)
        self.mouse.makeMoveable(1,1,.2,keyboard)
    def coord(self): return (self.mouse.pixels[0].x,self.mouse.pixels[0].y-1)
    def kill(self):
        self.mouse.kill()
        self.field.kill()
    def notify(self,coord): 
        assistant.read().soundEffect('click')
        self.kill()
        screen.read().clean()
        if self.coord() == (1,1): 
            a = decide([screen.read().letters[screen.read().letter_index.index("#")].paint(Color(100,0,50)),screen.read().letters[screen.read().letter_index.index("#")].paint(Color(0,50,100))],keyboard)
            b = decide([screen.read().letters[screen.read().letter_index.index("·")].paint(Color(50,50,50)),screen.read().letters[screen.read().letter_index.index("+")].paint(Color(50,50,50))],keyboard,right=2)
            c = decide([screen.read().letters[screen.read().letter_index.index("0")].paint(Color(100,200,0)),screen.read().letters[screen.read().letter_index.index("1")].paint(Color(100,200,0))],keyboard,right=2)
            d = decide([screen.read().letters[screen.read().letter_index.index("0")].paint(Color(100,0,200)),screen.read().letters[screen.read().letter_index.index("1")].paint(Color(100,0,200))],keyboard,right=2)
            Snake(1-b,c,d,1-a)
        if self.coord() == (1,3): 
            a,b,c = 0,decide([screen.read().letters[screen.read().letter_index.index("1")].paint(Color(0,0,255)),screen.read().letters[screen.read().letter_index.index("2")].paint(Color(0,0,255))],keyboard,right=3),4
            if b!=1: a = decide([screen.read().letters[screen.read().letter_index.index("x")].paint(Color(0,255,0)),screen.read().letters[screen.read().letter_index.index("0")].paint(Color(255,0,0))],keyboard,right=3)
            if b!=1: c = decide([screen.read().letters[screen.read().letter_index.index("1")].paint(Color(0,255,0)),screen.read().letters[screen.read().letter_index.index("2")].paint(Color(100,200,0)),screen.read().letters[screen.read().letter_index.index("3")].paint(Color(150,150,0)),screen.read().letters[screen.read().letter_index.index("4")].paint(Color(200,100,0)),screen.read().letters[screen.read().letter_index.index("5")].paint(Color(255,0,0))],keyboard,right=3)
            TresEnRaya(a,b,c)
        if self.coord() == (1,5): 
            a = decide([screen.read().letters[screen.read().letter_index.index("#")].paint(Color(0,255,0)),screen.read().letters[screen.read().letter_index.index("#")].paint(Color(255,0,0))],keyboard)
            Jump(a)
        if self.coord() == (3,1): 
            Chess()
        if self.coord() == (3,3): 
            Bar()

class Bar:
    def __init__(self):
        self.bar,self.ball,self.irrompible,self.wall,self.air = 4,3,2,1,0

        level = [
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [5,5,5,5,5,5,5,5],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,4,4,4,0,0]]

        self.vx,self.vy = -1,1
        self.cx,self.cy = 7,5

        self.grid = [[2 for i in range(8+2)]] + [[2] + i + [2] for i in level] + [[2 for i in range(10+2)]]

        self.grid[8][0],self.grid[8][9] = 0,0
        self.grid[self.cx][self.cy] = 3
        self.direction = 0

        self.show()
        while True:
            if keyboard.key[2]: 
                self.vy = -1
                break
            if keyboard.key[3]: 
                self.change(1)
                break
            time.sleep(0.1)

        while True:
            if keyboard.key[2]: self.change(0)
            if keyboard.key[3]: self.change(1)
            self.move()
            self.show()
            time.sleep(.2)
            self.move_bar(self.direction)
            if self.cx == 8: break
        Menu()

    def show(self):
        m3 = self.grid[1:9]
        m2 = [i[1:9] for i in m3]
        m = [[[Color(0,0,1),Color(200,100,0),Color(0,100,200),Color(0,255,0),Color(0,0,255),Color(255,0,0)][j] for j in i] for i in m2]
        screen.read().show(m)
        '''
        for i in range(1,8+1):
            text = ""
            for j in range(1,8+1): text += " █#¯"[self.grid[i][j]]
            print(text)'''

    #1 --> wall
    #0 --> air

    def move(self):
        if self.grid[self.cx+self.vx][self.cy]:
            if self.grid[self.cx+self.vx][self.cy] == 1:
                self.grid[self.cx+self.vx][self.cy] = 0
            if self.grid[self.cx+self.vx][self.cy] == 5:
                self.grid[self.cx+self.vx][self.cy] = 1
            self.vx *= -1
            self.move()
        elif self.grid[self.cx][self.cy+self.vy]:
            if self.grid[self.cx][self.cy+self.vy] == 1:
                self.grid[self.cx][self.cy+self.vy] = 0
            if self.grid[self.cx][self.cy+self.vy] == 5:
                self.grid[self.cx][self.cy+self.vy] = 1
            self.vy *= -1
            self.move()
        elif self.grid[self.cx+self.vx][self.cy+self.vy]:
            if self.grid[self.cx+self.vx][self.cy+self.vy] == 1:
                self.grid[self.cx+self.vx][self.cy+self.vy] = 0
            if self.grid[self.cx+self.vx][self.cy+self.vy] == 5:
                self.grid[self.cx+self.vx][self.cy+self.vy] = 1
            self.vx *= -1
            self.vy *= -1
            self.move()
        else:
            self.grid[self.cx][self.cy] = 0
            self.cx += self.vx
            self.cy += self.vy
            self.grid[self.cx][self.cy] = 3

    def move_bar(self,d):
        try:
            if d == 0 and self.grid[8][1] != 4:
                for i in range(9):
                    if self.grid[8][i+1] == 4 and self.grid[8][i] == 0: self.grid[8][i] = 4
                    if self.grid[8][i+1] == 0 and self.grid[8][i] == 4: self.grid[8][i] = 0
            if d == 1 and self.grid[8][8] != 4:
                for i in range(9,0,-1):
                    if self.grid[8][i-1] == 4 and self.grid[8][i] == 0: self.grid[8][i] = 4
                    if self.grid[8][i-1] == 0 and self.grid[8][i] == 4: self.grid[8][i] = 0
            time.sleep(.05)
        except: pass

    def change(self,n):
        self.direction = n


class Chess:
    def __init__(self):
        self.field = Field(screen.read())
        self.white_matrix = [["R","N","B","Q","K","B","N","R"],["P","P","P","P","P","P","P","P"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"]]
        self.black_matrix = [["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0"],["P","P","P","P","P","P","P","P"],["R","N","B","Q","K","B","N","R"]]
        self.white_pieces = [Pixel((-1,-1),Color(100,100,100),(-2,-2,8,8)) for i in range(16)]
        self.black_pieces = [Pixel((-1,-1),Color(100,100,100),(-2,-2,8,8)) for i in range(16)]
        self.game = lichess_game()
        self.show()
        self.mouse = Object([Pixel((5,5),6579300,(-1,-1,8,8))],t=1,func=self.notify)
        for piece in self.white_pieces: self.field.add(piece)
        for piece in self.black_pieces: self.field.add(piece)
        self.field.addObj(self.mouse)
        self.mouse.makeMoveable(1,1,.2,keyboard)
        self.mouse.paintC = Color(50,50,50)
        self.select = (-1,-1)
        if self.game.c == 1: 
            time.sleep(1)
            m = None
            while m == None: m = self.game.load()
            self.move(1-self.game.c,self.chess2coord(m[0]),self.chess2coord(m[1]))
    def coord(self): return (self.mouse.pixels[0].x,self.mouse.pixels[0].y-1)
    def kill(self):
        self.mouse.kill()
        self.field.kill()
    def notify(self,coord): 
        if self.game.c == 1: coord = (7-coord[0],7-coord[1])
        if self.select == coord: 
            self.mouse.paintC = Color(50,50,50)
            self.select = (-1,-1)
        elif self.select == (-1,-1): 
            self.select = coord
            self.mouse.paintC = Color(200,200,200)
        else:
            self.mouse.paintC = Color(50,50,50)
            move = self.coord2chess(self.select,coord)
            n = self.game.play(move)
            if n != 0: 
                self.move(self.game.c,self.select,coord)
                m = self.game.wait()
                self.move(1-self.game.c,self.chess2coord(m[0]),self.chess2coord(m[1]))
            self.select = (-1,-1)
    def chess2coord(self,chess): return ("abcdefgh".index(chess[0]),8-int(chess[1]))
    def move(self,c,c1,c2):
        if c == 0:
            self.white_matrix[7-c2[1]][c2[0]] = self.white_matrix[7-c1[1]][c1[0]]
            self.white_matrix[7-c1[1]][c1[0]] = "0"
            self.black_matrix[7-c2[1]][c2[0]] = "0"
        if c == 1:
            self.black_matrix[7-c2[1]][c2[0]] = self.black_matrix[7-c1[1]][c1[0]]
            self.black_matrix[7-c1[1]][c1[0]] = "0"
            self.white_matrix[7-c2[1]][c2[0]] = "0"
        self.show()
        self.field.move()
    def coord2chess(self,coord1,coord2): return "abcdefgh"[coord1[0]]+str(8-coord1[1])+"abcdefgh"[coord2[0]]+str(8-coord2[1])
    def show(self):
        c1 = 0
        c2 = 0
        for i in range(8):
            for j in range(8):
                if self.white_matrix[7-j][i] != "0":
                    piece = self.white_pieces[c1] 
                    if self.game.c == 0:
                        piece.x = i
                        piece.y = j
                    else:
                        piece.x = 7-i
                        piece.y = 7-j
                    piece.c = [Color(200,200,0),Color(0,200,200),Color(200,0,200),Color(50,50,255),Color(50,255,50),Color(255,50,50)]["PBNRKQ".index(self.white_matrix[7-j][i])]
                    c1+=1
                if self.black_matrix[7-j][i] != "0":
                    piece = self.black_pieces[c2] 
                    if self.game.c == 0:
                        piece.x = i
                        piece.y = j
                    else:
                        piece.x = 7-i
                        piece.y = 7-j
                    piece.c = [Color(100,50,0),Color(0,50,100),Color(100,0,50),Color(0,0,150),Color(0,150,0),Color(150,0,0)]["PBNRKQ".index(self.black_matrix[7-j][i])]
                    c2+=1
        screen.read().clean()

class Jump:
    def __init__(self,t):
        self.t = t
        self.contador = 0
        self.field = Field(screen.read())
        self.obj = [Object([Pixel((10,6),Color(0,0,255)),Pixel((11,6),Color(0,0,255))],t=1,func=self.new),Object([Pixel((11,6),Color(0,0,255)),Pixel((12,6),Color(0,0,255))],t=1,func=self.new),Object([Pixel((14,6),Color(0,0,255)),Pixel((15,6),Color(0,0,255))],t=1,func=self.new),Object([Pixel((17,6),Color(0,0,255)),Pixel((18,6),Color(0,0,255))],t=1,func=self.new)]
        if self.t == 1: 
            for i in range(1): self.obj.append(Object([Pixel((11,6),Color(0,0,255)),Pixel((12,6),Color(0,0,255))],t=1,func=self.new))
        for i in self.obj: 
            if self.obj.index(i) != 0 or self.t == 0: self.new(i)
        self.mouse = Object([Pixel((1,6),6579300,(-1,-1,7,7)),Pixel((1,5),6579300,(-1,-1,7,7))],t=1,nu=(0,-1),func=self.stand,func2=self.shift)
        if self.t == 1:
            self.mouse.move(0,-4,save=1)
        self.land = Object([Pixel((0,7),Color(0,255,0)),Pixel((1,7),Color(0,255,0)),Pixel((2,7),Color(0,255,0)),Pixel((3,7),Color(0,255,0)),Pixel((4,7),Color(0,255,0)),Pixel((5,7),Color(0,255,0)),Pixel((6,7),Color(0,255,0)),Pixel((7,7),Color(0,255,0))],t=1,nu=(0,-1))
        self.field.addObj(self.mouse),self.field.addObj(self.land)
        self.mouse.makeMoveable(1,1,.1,keyboard,t=1)
        if self.t == 1:
            self.mouse.p = -4
            self.mouse.h = 4
            self.mouse.u = 0
            for i in self.land.pixels: i.c = Color(255,0,0)
        self.accel=0
        for i in self.obj: 
            self.field.addObj(i)
            i.makeMoveable(1,1,.1,keyboard,t=2)
        self.thread = Thread(self.loop,loop=True)
        self.thread.start()
    def coord(self): return (self.mouse.pixels[0].x,self.mouse.pixels[0].y-1)
    def kill(self):
        self.thread.pause()
        time.sleep(.1)
        self.mouse.kill()
        self.field.kill()
        for i in self.obj: i.kill()
    def stand(self,coord): 
        self.mouse.pixels[1].x,self.mouse.pixels[1].y = coord[0]-1,coord[1]+1
        screen.read().pixel((coord[0],coord[1]),Color(0,0,1),save=False,show=False)
        self.revise()
    def shift(self,coord): 
        self.mouse.pixels[1].x,self.mouse.pixels[1].y = coord[0],coord[1]
        screen.read().pixel((coord[0]-1,coord[1]+1),Color(0,0,1),save=False,show=False)
        self.revise()
    def revise(self):
        r,tp,b=0,0,0
        if self.field.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=Color(0,255,0),color3=6579300) == False and self.field.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=6579300): 
            self.mouse.move(0,-1,save=1)
            self.mouse.h += 1
        if self.field.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=6579300,color3=Color(100,200,0)): r=1
        if self.field.pixelOn((self.mouse.pixels[1].x,self.mouse.pixels[1].y),color=6579300,color3=Color(100,200,0)): r=1
        if self.field.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=6579300,color3=Color(200,0,100)): tp=1
        if self.field.pixelOn((self.mouse.pixels[1].x,self.mouse.pixels[1].y),color=6579300,color3=Color(200,0,100)): tp=1
        if self.field.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=6579300,color3=Color(255,0,0)): b=1
        if self.field.pixelOn((self.mouse.pixels[1].x,self.mouse.pixels[1].y),color=6579300,color3=Color(255,0,0)): b=1
        if r and b == 0 or self.field.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=6579300) and self.field.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=6579300,color3=Color(0,0,255))==False or self.field.pixelOn((self.mouse.pixels[1].x,self.mouse.pixels[1].y),color=6579300) and self.field.pixelOn((self.mouse.pixels[1].x,self.mouse.pixels[1].y),color=6579300,color3=Color(0,0,255))==False: 
            self.kill()
            assistant.read().soundEffect('loose')
            screen.read().text("Distancia: "+str(self.contador)+'m ',speed=.1,fg=Color(255,0,0))
            time.sleep(8)
            screen.read().clean()
            Menu()
        if tp and r == 0: 
            self.kill()
            screen.read().clean()
            m = Jump(1-self.t)
            assistant.read().soundEffect('click')
            time.sleep(1)
            m.contador += self.contador
        if b and tp == 0: 
            self.contador += 50*(1+self.t*2)
            print("+"+str(50*(1+self.t*2))+" points")
    def new(self,obj,t=None):
        for i in obj.pixels:
            self.field.remove(i)
        c = [Color(0,0,255),[Color(255,0,0),Color(0,255,0)][self.t]][random.randint(0,1)]
        n = random.randint(8,20+(1-self.t)*10)
        p = []
        if t == None: t = random.randint(0,7)
        if t == 0:
            p.append(Pixel((n,6-self.t),c))
            if self.t == 0: p.append(Pixel((n,5),c))
            else: p.append(Pixel((n+1,5),c))
        elif t == 1:
            p.append(Pixel((n,6),c))
            p.append(Pixel((n,5),c))
            p.append(Pixel((n+1,6),c))
            p.append(Pixel((n+1,5),c))
        elif t == 2:
            p.append(Pixel((n,6),c))
        elif t == 3:
            p.append(Pixel((n,5),c))
        elif t == 4:
            p.append(Pixel((n,4),c))
        elif t == 5:
            c = [Color(0,255,0),c][self.t]
            p.append(Pixel((n,6),c))
            p.append(Pixel((n+1,6),c))
        elif t == 6:
            c = Color(200,0,100)
            p.append(Pixel((n,2),c))
        elif t == 7:
            c = Color(100,200,0)
            p.append(Pixel((n,1),c))
        if self.field.pixelOn((p[0].x,p[0].y),color=6579300)==False:
            if len(p)>1:
                if self.field.pixelOn((p[1].x,p[1].y),color=6579300)==True: pass
                else:
                    for i in p:
                        self.field.add(i)
                    obj.pixels = p
            else:
                for i in p:
                    self.field.add(i)
                obj.pixels = p
        else: self.new(obj,t=t)
    def loop(self):
        self.contador += 1+self.t*2
        screen.read().strip.show()
        time.sleep(.2-self.accel)
        screen.read().strip.show()
        for i in self.obj: i.update()
        self.mouse.update()
        self.field.move((10,10),(10,11))
        if self.accel < 0.19: self.accel+=.001

class TresEnRaya:
    def __init__(self,f=0,j=0,d=4):
        self.field = Field(screen.read())
        self.p = [Pixel((1,1),Color(0,0,255)),Pixel((3,1),Color(0,0,255)),Pixel((5,1),Color(0,0,255)),Pixel((1,3),Color(0,0,255)),Pixel((3,3),Color(0,0,255)),Pixel((5,3),Color(0,0,255)),Pixel((1,5),Color(0,0,255)),Pixel((3,5),Color(0,0,255)),Pixel((5,5),Color(0,0,255))]
        self.coords = [(1,1),(3,1),(5,1),(1,3),(3,3),(5,3),(1,5),(3,5),(5,5)]
        self.mouse = Object([Pixel((6,7),6579300,(0,1,7,8)),Pixel((7,6),6579300,(1,0,8,7)),Pixel((6,5),6579300,(0,-1,7,6)),Pixel((5,6),6579300,(-1,0,6,7))],t=1,nu=(0,-1),func=self.notify)
        self.field.addObj(self.mouse)
        for i in self.p: self.field.add(i)
        self.mouse.makeMoveable(1,1,.2,keyboard,color2=Color(0,0,255))
        self.left = [0,1,2,3,4,5,6,7,8]
        if f == 1 and j == 0: 
            time.sleep(2)
            if d>2: p2 = self.p[[0,2,4,4,4,4,4,6,8][random.randint(0,8)]]
            else: p2 = self.p[random.randint(0,8)]
            p2.c = Color(255,0,0)
            self.left.remove( self.index(p2))
            screen.read().pixel((p2.x,p2.y),Color(255,0,0),0,1)
        self.j = j
        self.t = 0
        self.d = d
    def pixelAt(self,c): return self.p[self.coords.index(c)]
    def coord(self): return (self.mouse.pixels[0].x,self.mouse.pixels[0].y-1)
    def index(self,p): return self.p.index(p)
    def copy(self,list):
        r = []
        for i in list: r.append(i)
        return r
    def types(self,p=0):
        m = [0,0,0,0,0,0,0,0,0]
        for i in range(9):
            if self.p[i].c == Color(255,0,0): m[i] = 2-p
            if self.p[i].c == Color(0,255,0): m[i] = 1+p
            if self.p[i].c == Color(0,0,255): m[i] = 0
        return m
    def move(self,left):
        d = self.d
        print(d)
        n = self.p[left[random.randint(0,len(left)-1)]]
        if self.willWin(left,1) and d>0:
            print("W1")
            n = self.p[left[0]]
            for i in left:
                self.p[i].c = Color(255,0,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.win(1): 
                    n = self.p[i]
                self.p[i].c = Color(0,0,255)
        elif d>3 and len(left) == 8 and 4 not in left: 
            print("OK")
            n = self.p[[2,0,6,8][random.randint(0,3)]]
        elif d>3 and len(left) == 8 and 2 not in left or len(left) == 8 and 0 not in left or len(left) == 8 and 6 not in left or len(left) == 8 and 8 not in left: n = self.p[4]
        elif self.willLoose(left,1) and d>0:
            print("L1")
            n = self.p[left[0]]
            for i in left:
                self.p[i].c = Color(0,255,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.win(0): 
                    n = self.p[i]
                self.p[i].c = Color(0,0,255)
        elif self.willWin(left,2) and d>1:
            print("W2")
            for i in left:
                self.p[i].c = Color(255,0,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.win(1,1,left2): n = self.p[i]
                self.p[i].c = Color(0,0,255)
        elif self.willLoose(left,2) and d>1:
            print("L2")
            for i in left:
                self.p[i].c = Color(255,0,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.willLoose(left2,2) == 0: n = self.p[i]
                self.p[i].c = Color(0,0,255)
        elif self.willWin(left,3) and d>3:
            print("W3")
            for i in left:
                self.p[i].c = Color(255,0,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.win(1,2,left2): n = self.p[i]
                self.p[i].c = Color(0,0,255)
        elif self.willLoose(left,3) and d>3:
            print("L3")
            for i in left:
                self.p[i].c = Color(255,0,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.willLoose(left2,3) != 1: n = self.p[i]
                self.p[i].c = Color(0,0,255)
        return n
    def win(self,p=0,t=0,left=None):
        if left == None: left = self.left
        m = self.types(p)
        r = 0
        if t == 0:
            if m[0] == 1 and m[3] == 1 and m[6] == 1 or m[0] == 1 and m[1] == 1 and m[2] == 1 or m[0] == 1 and m[4] == 1 and m[8] == 1 or m[2] == 1 and m[4] == 1 and m[6] == 1 or m[1] == 1 and m[4] == 1 and m[7] == 1 or m[2] == 1 and m[5] == 1 and m[8] == 1 or m[3] == 1 and m[4] == 1 and m[5] == 1 or m[6] == 1 and m[7] == 1 and m[8] == 1:
                r = 1
        if t == 1:
            if p == 0:
                v = 0
                if self.willWin(left) != 1: v += 1
                for i in left:
                    self.p[i].c = Color(0,255,0)
                    if self.win(0): v += 1
                    self.p[i].c = Color(0,0,255)
                if v == 3: r = 1
            if p == 1:
                v = 0
                if self.willLoose(left) != 1: 
                    v += 1
                for i in left:
                    self.p[i].c = Color(255,0,0)
                    if self.win(1): v += 1
                    self.p[i].c = Color(0,0,255)
                if v == 3: r = 1
        if t == 2:
            if p == 0:
                v1,v2,v3 = 0,0,0
                p = 0
                if self.willWin(left) != 1: 
                    v1 = 1
                for i in left:
                    self.p[i].c = Color(0,255,0)
                    if self.win(0): 
                        v2 = 1
                        if i in left: p = i
                    left2 = self.copy(left)
                    left2.remove(i)
                    if self.win(0,1,left2): 
                        v3 = 1
                    self.p[i].c = Color(0,0,255)
                    if p == i: self.p[i].c = Color(255,0,0)
                self.p[p].c = Color(0,0,255)
                if v1+v2+v3 == 3: r = 1
            if p == 1:
                v1,v2,v3 = 0,0,0
                p = 0
                if self.willLoose(left) != 1: v1 = 1
                for i in left:
                    self.p[i].c = Color(255,0,0)
                    if self.win(1): 
                        v2 = 1
                        if i in left: p = i
                    left2 = self.copy(left)
                    left2.remove(i)
                    if self.win(1,1,left2): v3 = 1
                    self.p[i].c = Color(0,0,255)
                    if p == i: self.p[i].c = Color(0,255,0)
                self.p[p].c = Color(0,0,255)
                if v1+v2+v3 == 3: r = 1
        return r
    def kill(self):
        self.mouse.kill()
        self.field.kill()
    def willLoose(self,left,t=1):
        r = 0
        if t == 1:
            for i in left:
                self.p[i].c = Color(0,255,0)
                if self.win(0): r = 1
                self.p[i].c = Color(0,0,255)
        if t == 2:
            for i in left:
                self.p[i].c = Color(0,255,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.win(0,1,left2): r = 1
                self.p[i].c = Color(0,0,255)
        if t == 3:
            for i in left:
                self.p[i].c = Color(0,255,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.win(0,2,left2): r = 1
                self.p[i].c = Color(0,0,255)
        return r
    def willWin(self,left,t=1):
        r = 0
        if t == 1:
            for i in left:
                self.p[i].c = Color(255,0,0)
                if self.win(1): r = 1
                self.p[i].c = Color(0,0,255)
        if t == 2:
            for i in left:
                self.p[i].c = Color(255,0,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.win(1,1,left2): r = 1
                self.p[i].c = Color(0,0,255)
        if t == 3:
            for i in left:
                self.p[i].c = Color(255,0,0)
                left2 = self.copy(left)
                left2.remove(i)
                if self.win(1,2,left2): r = 1
                self.p[i].c = Color(0,0,255)
        return r
    def notify(self,coord): 
        assistant.read().soundEffect('click')
        j = self.j
        p = self.pixelAt(self.coord())
        if p.c == Color(0,0,255): 
            if j == 0 or self.t == 0:
                p.c = Color(0,255,0)
                self.t = 1
                if j == 1: self.mouse.paintC = Color(255,0,0)
            else:
                p.c = Color(255,0,0)
                self.t = 0
                self.mouse.paintC = Color(0,255,0)
            self.left.remove(self.index(p))
            if self.win(p=0): 
                assistant.read().soundEffect('win')
                self.kill()
                screen.read().text("WINS J1         ",fg=Color(0,255,0))
                time.sleep(6)
                Menu()
            if len(self.left) != 0: 
                if j == 0:
                    screen.read().pixel((p.x,p.y),Color(0,255,0),0,1)
                    time.sleep(2)
                    p2 = self.move(self.left)
                    p2.c = Color(255,0,0)
                    self.left.remove( self.index(p2))
                    screen.read().pixel((p2.x,p2.y),Color(255,0,0),0,1)
                    if len(self.left) == 0: 
                        self.kill()
                        assistant.read().soundEffect('bip')
                        screen.read().text("TIE         ",fg=Color(0,0,255))
                        time.sleep(6)
                        Menu()
            else:
                self.kill()
                assistant.read().soundEffect('bip')
                screen.read().text("TIE         ",fg=Color(0,0,255))
                time.sleep(6)
                Menu()
            if self.win(p=1):
                time.sleep(2)
                self.kill()
                assistant.read().soundEffect('loose')
                screen.read().text("WINS J2         ",fg=Color(255,0,0))
                time.sleep(6)
                Menu()

def decide(options,kb,right=0):
    var = None
    screen.read().show(options[0],right)
    active = 0
    min,max = 0,len(options)-1
    while var == None:
        time.sleep(.2)
        if kb.key[3]: active += 1
        if kb.key[2]: active -= 1
        if active > max: active = min
        if active < min: active = max
        screen.read().show(options[active],right)
        if kb.key[4]: var = active
    assistant.read().soundEffect('select')
    screen.read().clean()
    return var

class Snake:
    def __init__(self,diagonal=1,teleport=1,move=0,rainbow=0,delay=.2):
        self.field = Field(screen.read())
        self.rainbow = rainbow
        self.p = Pixel(self.pixelCoord(),[Color(255,0,0),Color(200,100,0),Color(0,255,0),Color(100,100,100),Color(200,0,100)][random.randint(0,4)],(-1,-1,8,8))
        if rainbow:
            if teleport: self.mouse = Chain([Pixel((6,6),Color(0,0,255),(0,0,7,7),teleport=teleport),Pixel((6,5),Color(0,100,100),(0,0,7,7))],t=2,func=self.notify,move=move)
            else: self.mouse = Chain([Pixel((6,6),Color(0,0,255),(-1,-1,8,8),teleport=teleport),Pixel((6,5),Color(0,100,100),(0,0,7,7))],t=2,func=self.notify,move=move)
        else:
            if teleport: self.mouse = Chain([Pixel((6,6),Color(0,0,255),(0,0,7,7),teleport=teleport),Pixel((6,5),Color(0,100,100),(0,0,7,7)),Pixel((6,4),Color(0,100,100),(0,0,7,7)),Pixel((6,3),Color(0,100,100),(0,0,7,7))],t=2,func=self.notify,move=move)
            else: self.mouse = Chain([Pixel((6,6),Color(0,0,255),(-1,-1,8,8),teleport=teleport),Pixel((6,5),Color(0,100,100),(0,0,7,7)),Pixel((6,4),Color(0,100,100),(0,0,7,7)),Pixel((6,3),Color(0,100,100),(0,0,7,7))],t=2,func=self.notify,move=move)
        self.field.add(self.p)
        self.field.addObj(self.mouse)
        self.mouse.makeMoveable(1,1,delay,keyboard,diagonal=diagonal)
        time.sleep(1)
    def notify(self): 
        if self.mouse.pixels[0].boss.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=Color(0,0,255),color2=Color(255,0,0)):
            assistant.read().soundEffect('bip')
            if self.rainbow: self.mouse.pixels.append(Pixel((self.mouse.pixels[len(self.mouse.pixels)-1].x,self.mouse.pixels[len(self.mouse.pixels)-1].y),self.p.c,(0,0,7,7)))
            else: self.mouse.pixels.append(Pixel((self.mouse.pixels[len(self.mouse.pixels)-1].x,self.mouse.pixels[len(self.mouse.pixels)-1].y),Color(0,100,100),(0,0,7,7)))
            self.field.add(self.mouse.pixels[len(self.mouse.pixels)-1])
            self.p.c = [Color(255,0,0),Color(200,100,0),Color(0,255,0),Color(100,100,100),Color(200,0,100)][random.randint(0,4)]
            self.p.x,self.p.y = self.pixelCoord()
        if self.mouse.pixels[0].boss.pixelOn((self.mouse.pixels[0].x,self.mouse.pixels[0].y),color=Color(0,0,255),color2=Color(0,100,200)) or self.mouse.pixels[0].x > 7 or self.mouse.pixels[0].x < 0 or self.mouse.pixels[0].y > 7 or self.mouse.pixels[0].y < 0:
            assistant.read().soundEffect('loose')
            self.mouse.kill()
            self.field.kill()
            screen.read().text("game over !         ",fg=Color(255,0,0))
            time.sleep(6)
            Menu()
    def pixelCoord(self):
        try:
            x,y = random.randint(0,7),random.randint(0,7)
            if self.field.pixelOn((x,y)): x,y = self.pixelCoord()
            return (x,y)
        except:
            assistant.read().soundEffect('win')
            self.mouse.kill()
            self.field.kill()
            screen.read().text("!!!         ",fg=Color(0,255,0))
            time.sleep(6)
            Menu()

if __name__ == "__main__":
    screen.write(Screen())
    Menu()
    while True: pass