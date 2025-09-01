from Thread import Runner, Thread

from rpi_ws281x import PixelStrip, Color
import time 


class Screen(Runner):
    def __init__(self):
        super(Screen,self).__init__(None)
    def init(self):
        self.strip = PixelStrip(64, 18, 800000, 10, False, 12, 0)
        self.strip.begin()
        self.mem = self.Matrix([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],Color(1,1,1))
        self.rt = 1
        self.rs = 1
        self.rc = False
        self.rainbowThread = Thread(self.rainbowColorFunc,loop=True,param=(1)) # Replaces 000000 by a rainbow color
        self.rainbowThread.start()
        self.queue = 0
        self.activeThread = 0
        self.animThread = None
        self.activeAnimThread = 0
        self.letters = []
        self.letter_caps  = " ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        self.letter_index = " abcdefghijklmnñopqrstuvwxyz0123456789.!:()+-·&$#¬"
        self.letters_accents = ["áéíóú","ÁÉÍÓÚ","aeiou"]
        self.letters.append(self.Matrix([[0],[0],[0],[0],[0],[0],[0],[0]])) # ALL CHARACTERS PIXELS
        self.letters.append(self.Matrix([[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,1,1,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[0,1,1,1],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[0,1,1,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,1,1,1],[1,0,0,0],[1,1,1,0],[1,0,0,0],[1,0,0,0],[1,1,1,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,1,1,1],[1,0,0,0],[1,1,1,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,0],[1,0,1,1],[1,0,0,1],[0,1,1,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[1,1,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,1,1,1],[0,0,0,1],[0,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,0,0,1],[1,0,1,0],[1,1,0,0],[1,1,0,0],[1,0,1,0],[1,0,0,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0,0],[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0,0],[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1],[1,0,0,0,1],[0,0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1],[0,0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,1,1],[1,0,0,1],[0,1,1,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,1,0,0],[1,0,1,0],[1,0,0,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[0,1,1,1],[1,0,0,0],[0,1,1,0],[0,0,0,1],[0,0,0,1],[1,1,1,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,1,0,1],[1,1,0,1,1],[1,0,0,0,1],[0,0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,0,1],[1,0,1],[0,1,0],[1,0,1],[1,0,1],[1,0,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,0,1],[1,0,1],[1,0,1],[0,1,0],[0,1,0],[0,1,0],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0,0],[1,1,1,1],[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0],[1,1,1,1],[0,0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[0,0,1],[0,1,1],[1,0,1],[0,0,1],[0,0,1],[0,0,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[1,0,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[0,0,1],[0,1,1],[0,0,1],[0,0,1],[1,1,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[0,0,1],[0,1,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[1,0,0],[1,1,1],[0,0,1],[0,0,1],[1,1,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[1,0,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[0,0,1],[0,0,1],[0,1,1],[0,0,1],[0,0,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,0,1],[1,1,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[1,1,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,0]]))
        self.letters.append(self.Matrix([[0],[0],[0],[0],[0],[0],[1],[0]]))
        self.letters.append(self.Matrix([[0],[1],[1],[1],[1],[0],[1],[0]]))
        self.letters.append(self.Matrix([[0],[0],[1],[0],[0],[1],[0],[0]]))
        self.letters.append(self.Matrix([[0,0],[0,1],[1,0],[1,0],[1,0],[1,0],[0,1],[0]]))
        self.letters.append(self.Matrix([[0,0],[1,0],[0,1],[0,1],[0,1],[0,1],[1,0],[0]]))
        self.letters.append(self.Matrix([[0,0,0],[0,0,0],[0,1,0],[1,1,1],[0,1,0],[0,0,0],[0,0,0],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[0,0,0],[0,0,0],[1,1,1],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]))
        self.letters.append(self.Matrix([[0,0,0],[0,0,0],[1,0,1],[0,1,0],[1,0,1],[0,0,0],[0,0,0],[0,0,0]]))
        self.letters.append(self.Matrix([[0,1,1,0,0,1,1,0],[1,1,1,0,0,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[0,1,1,1,1,1,1,0],[0,0,1,1,1,1,0,0],[0,0,0,1,1,0,0,0]]))
        self.letters.append(self.Matrix([[0,1,1,1,1,0,0,0],[0,0,0,0,0,1,0,0],[0,1,1,1,0,0,1,0],[0,0,0,0,1,0,0,1],[0,1,1,0,0,1,0,1],[0,0,0,1,0,1,0,1],[1,1,0,1,0,1,0,1],[1,1,0,0,0,0,0,0]]))
        self.letters.append(self.Matrix([[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]))
        self.letters.append(self.Matrix([[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0]]))
        (self.amongus1) = (self.Matrix([[0,0,0,0,0,0,0,0],[0,0,0,1,1,1,0,0],[0,1,1,1,1,0,0,0],[0,1,1,1,1,0,0,0],[0,1,1,1,1,1,1,0],[0,0,0,1,1,1,0,0],[0,0,1,1,0,1,1,0],[0,0,0,0,0,0,0,0]]))
        (self.amongus2) = (self.Matrix([[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,0,0,1],[1,1,1,1,1,0,0,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]))
        self.ps4 = [[Color(0, 0, 1), Color(0, 0, 1), Color(0, 0, 1), Color(64, 224, 208), Color(64, 224, 208), Color(0, 0, 1), Color(0, 0, 1), Color(0, 0, 1)], [Color(0, 0, 1), Color(0, 0, 1), Color(64, 224, 208), Color(0, 255, 0), Color(0, 255, 0), Color(64, 224, 208), Color(0, 0, 1), Color(0, 0, 1)], [Color(0, 0, 1), Color(64, 224, 208), Color(0, 255, 0), Color(255, 0, 0), Color(255, 0, 0), Color(0, 255, 0), Color(64, 224, 208), Color(0, 0, 1)], [Color(0, 0, 1), Color(64, 224, 208), Color(0, 255, 0), Color(255, 105, 180), Color(255, 105, 180), Color(0, 255, 0), Color(64, 224, 208), Color(0, 0, 1)], [Color(64, 224, 208), Color(64, 224, 208), Color(255, 105, 180), Color(255, 255, 255), Color(255, 255, 255), Color(255, 105, 180), Color(64, 224, 208), Color(64, 224, 208)], [Color(64, 224, 208), Color(64, 224, 208), Color(255, 105, 180), Color(255, 255, 255), Color(255, 255, 255), Color(255, 105, 180), Color(64, 224, 208), Color(64, 224, 208)], [Color(0, 0, 1), Color(0, 0, 1), Color(64, 224, 208), Color(64, 224, 208), Color(64, 224, 208), Color(64, 224, 208), Color(0, 0, 1), Color(0, 0, 1)], [Color(0, 0, 1), Color(0, 0, 1), Color(0, 0, 1), Color(64, 224, 208), Color(64, 224, 208), Color(0, 0, 1), Color(0, 0, 1), Color(0, 0, 1)]]
        self.animation = [] # ANIMATIONS (GROUP OF IMAGES)
        self.animation.append(self.Animation([[[1,0,0,1,1,0,0,1],[0,0,1,0,0,1,0,0],[0,1,0,0,0,0,1,0],[1,0,0,1,1,0,0,1],[0,0,1,0,0,1,0,0],[0,1,0,0,0,0,1,0],[1,0,0,1,1,0,0,1],[0,0,1,0,0,1,0,0]],[[0,0,1,0,0,1,0,0],[0,1,0,0,0,0,1,0],[1,0,0,1,1,0,0,1],[0,0,1,0,0,1,0,0],[0,1,0,0,0,0,1,0],[1,0,0,1,1,0,0,1],[0,0,1,0,0,1,0,0],[0,1,0,0,0,0,1,0]],[[0,1,0,0,0,0,1,0],[1,0,0,1,1,0,0,1],[0,0,1,0,0,1,0,0],[0,1,0,0,0,0,1,0],[1,0,0,1,1,0,0,1],[0,0,1,0,0,1,0,0],[0,1,0,0,0,0,1,0],[1,0,0,1,1,0,0,1]]],m=False))
        self.animation.append(self.Animation(self.animation[0].rotate(1),m=False))
        self.animation.append(self.Animation(self.animation[0].rotate(2),m=False))
        self.animation.append(self.Animation(self.animation[0].rotate(3),m=False))
        self.animation.append(self.Animation([[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,1,0,0],[0,0,1,1,1,1,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]],m=False))
        self.animation.append(self.Animation([[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,1,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[1,1,0,1,0,0,0,0],[1,1,0,0,0,0,0,0]],[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,1,1,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,1,0,0],[1,1,0,0,0,1,0,0],[1,1,0,0,0,0,0,0]],[[0,1,1,1,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,1],[1,1,0,0,0,0,0,1],[1,1,0,0,0,0,0,0]]],m=False))
        self.animation.append(self.Animation([[[0,0,0,0,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],
                                              [[0,0,0,0,0,0,0,0],[0,0,0,0,1,1,0,0],[0,0,0,0,1,1,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],
                                              [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,1,1,0],[0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],
                                              [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,1,1,0],[0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],
                                              [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,1,1,0,0],[0,0,0,0,1,1,0,0],[0,0,0,0,0,0,0,0]],
                                              [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,0,0,0,0,0,0]],
                                              [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,1,1,0,0,0,0,0],[0,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]],
                                              [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,1,1,0,0,0,0,0],[0,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]],m=False))
    def pixel(self,coord,color,save=True,show=False): # Register a pixel
        if coord[0] >= 0 and coord[0] <= 7:
            if color != Color(0,0,0): self.strip.setPixelColor(8*coord[1]+coord[0], color)
            if save: self.mem.matrix[coord[1]][coord[0]] = color
        if show: self.strip.show()
    def add(self,matrix): # Add matrix to the right (hidden)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                self.mem.matrix[i][j+8] = matrix[i][j]
    def show(self,matrix=None,right=0): # Show all pixels
        if matrix is None: matrix = self.mem.matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                self.pixel((j+right,i),matrix[i][j])
        self.strip.show()
    def clean(self): self.fill(Color(0,0,1))
    def pixel_art(self,image,key): # Show a pixel art on the screen
        output = [[Color(0,0,1) for j in range(8)] for i in range(8)]
        for i in range(len(image)):
            for j in range(len(image[i])):
                if image[i][j] not in ". " and i<8 and j<8:
                    output[i][j] = key[image[i][j]]
        self.show(output)
    def anim(self,animation,speed=.5): # Display an animation
        self.queue += 1
        queue = self.queue
        if self.activeAnimThread == 1:
            self.activeAnimThread = 0
            self.animThread.stop()
            self.activeThread += 1
            time.sleep(1)
        self.animThread = Thread(self.animFunc,loop=True,param=(animation,speed,queue))
        self.animThread.start()
    def animFunc(self,animation,speed,queue): 
        if self.activeThread == 0: self.activeThread = 1 # Wait for turn
        while self.activeThread != queue: pass
        self.activeAnimThread = 1
        for matrix in animation:
            self.show(matrix)
            time.sleep(speed)
    def text(self,text,fg=Color(0,100,200),bg=Color(0,0,1),speed=.3): # Show text passing through the screen
        self.queue += 1
        if fg != Color(0,0,0): text += " "
        queue = self.queue
        Thread(self.textFunc,param=(text,fg,bg,speed,queue)).start()
    def textFunc(self,text,fg,bg,speed,queue):
        if fg == Color(0,0,0): self.rc = True
        if self.activeThread == 0: self.activeThread = 1
        while self.activeThread != queue: 
            if self.activeAnimThread == 1: # Animations are endless, in such case, interrupt them
                self.activeAnimThread = 0
                self.animThread.stop()
                self.activeThread += 1
                time.sleep(1)
        if self.mem.matrix[0][0] != bg: self.fill(bg)
        for letter in text:
            self.show()
            self.mem.scroll()
            if letter in self.letter_caps: l = self.letters[self.letter_caps.index(letter)]
            elif letter in self.letters_accents[0]: l = self.letters[self.letter_index.index(self.letters_accents[2][self.letters_accents[0].index(letter)])]
            elif letter in self.letters_accents[1]: l = self.letters[self.letter_index.index(self.letters_accents[2][self.letters_accents[1].index(letter)])]
            else: l = self.letters[self.letter_index.index(letter)]
            self.add(l.paint(fg,bg))
            time.sleep(speed)
            for i in range(len(l.matrix[0])):
                if l == self.letters[0]: 
                    time.sleep(speed)
                    break
                self.show()
                self.mem.scroll()
                time.sleep(speed)
        self.rc = False
        self.activeThread += 1 # Next in the queue
    def fill(self,color): # Paint all the same color
        for i in range(17):
            for j in range(8):
                self.pixel((i,j),(color))
        self.strip.show()
    def number2pixel(self,n): # Transform number (64) to coord (8x8)
        y = 0
        while n >= 8:
            y+=1
            n-=8
        return n,y
    def colorWipe(self,color,wait=.05): # Animation
        for i in range(64):
            self.pixel(self.number2pixel(i),color)
            self.strip.show()
            time.sleep(wait)
    def wheel(self, pos): # Determine color (for rainbow)
        if pos < 85: return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170: return Color(255 - (pos-85) * 3, 0, (pos-85) * 3)
        else: return Color(0, (pos-170) * 3, 255 - (pos-170) * 3)
    def rainbow(self, iterations=1): # Animation
        for j in range(256 * iterations):
            for i in range(64):
                self.pixel(self.number2pixel(i), self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(1)
    def toogleRainbow(self,rt,rs=None): # Change rainbow mode
        if rs != None: self.rs = rs
        self.rt = rt
        self.rc = False
        if rt == 0: self.rainbowThread.pause()
        else: self.rainbowThread.resume()
    def rainbowColorFunc(self,iterations=1): # Paint 000000 pixels to their respective rainbow color
            for j in range(256 * iterations):
                for i in range(64):
                    if self.rt == 1: 
                        if self.mem.matrix[self.number2pixel(i)[1]][self.number2pixel(i)[0]] == Color(0,0,0): self.pixel(self.number2pixel(i), self.wheel((int(i) + j) & 255),save=False)
                    elif self.rt == 3: 
                        if self.mem.matrix[self.number2pixel(i)[1]][self.number2pixel(i)[0]] == Color(0,0,0): self.pixel(self.number2pixel(i), self.wheel((int((i + j)*4)) & 255),save=False)
                    else: 
                        if self.mem.matrix[self.number2pixel(i)[1]][self.number2pixel(i)[0]] == Color(0,0,0): self.pixel(self.number2pixel(i), self.wheel(j & 255),save=False)
                if self.rc:
                    for i in range(64):
                        if self.mem.matrix[self.number2pixel(i)[1]][self.number2pixel(i)[0]] == Color(0,0,1): self.pixel(self.number2pixel(i),Color(0,0,1),save=False)
                self.strip.show()
                time.sleep(0.1/self.rs)
    def show_hex(self,hex): # Display from a hex code with 64 values
        matrix = []
        for row in range(8):
            hex_row = hex[row*7*8:(1+row)*7*8]
            matrix_row = []
            for col in range(8):
                hex_col = hex_row[col*7+1:(1+col)*7]
                r,g,b = int(hex_col[:2],16),int(hex_col[2:4],16),int(hex_col[4:6],16)
                matrix_row.append(Color(r,g,b))
            matrix.append(matrix_row)
        self.show(matrix)
    def matrix_addition(self,m1,m2): # Add images
        r = m1
        for i in range(8):
            for j in range(8):
                if m1[i][j] == Color(0,0,1): r[i][j] = m2[i][j]
        return r
    def soundbar(self,n=0): self.show(self.soundbar_tool(n).paint(Color(0,0,0))) # Show a soundbar (for music animation)
    def wait_(self):
        self.queue += 1
        queue = self.queue
        if self.activeThread == 0: self.activeThread = 1
        while self.activeThread != queue: 
            if self.activeAnimThread == 1:
                self.activeAnimThread = 0
                self.animThread.stop()
                self.activeThread += 1
                time.sleep(.1)
        self.activeThread += 1
    def soundbar_tool(self,n=0):
        v1,v2 = [0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1]
        m = [v1,v1,v1,v1,v1,v1,v1,v1]
        if n > 0: 
            for i in range(n): m[7-i] = v2
        return self.Matrix(m)
    def amongus(self,n=0):
        m1 = self.Matrix(self.amongus1.rotate(n)).paint(Color(0,255,0))
        m1 = self.matrix_addition(m1, self.Matrix(self.amongus2.rotate(n)).paint(color1=Color(1,1,1),color2=Color(0,100,200)))
        self.show(m1)
    def bar(self,n=0):
        m1 = self.letters[self.letter_index.index("¬")].paint(Color(100,100,100))
        m1 = self.matrix_addition(m1,self.bar_tool(n).paint(Color(0,100,200)))
        self.show(m1)
    def bar_tool(self,n=0):
        v = [[0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,1,1,0,0,0,0,0],[0,1,1,1,0,0,0,0],[0,1,1,1,1,0,0,0],[0,1,1,1,1,1,0,0],[0,1,1,1,1,1,1,0]][n]
        return self.Matrix([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],v,v,v,v,[0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]])
    class Matrix: # 8x8 matrix
        def __init__(self, matrix, color=None):
            self.matrix = matrix
            if color is not None: self.matrix = self.paint(color)
        def paint(self, color1, color2=Color(0,0,1)): # replace bool by a color rule
            value = []
            for i in self.matrix:
                val = []
                for j in i:
                    if j == 1: val.append(color1)
                    else: val.append(color2)
                value.append(val)
            return value
        def scroll(self): # Scroll to the left
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[i])-1):
                    self.matrix[i][j] = self.matrix[i][j+1]
        def rotate(self,times): # Rotate 90º a determined amount of times
            r1 = self.matrix
            if times >= 2:
                times -= 2
                r2 = []
                for i in range(len(r1)): r2.append(r1[7-i])
            else: r2 = r1
            if times >= 1:
                r3 = []
                for i in range(8):
                    r3b = []
                    for j in range(8): r3b.append(r2[j][i])
                    r3.append(r3b)
            else: r3 = r2
            return r3
    class Animation:
        def __init__(self,animation,color=None,m=True):
            self.animation = animation
            if color is not None: self.animation = self.paint(color)
            self.m = m
        def paint(self, color1, color2=Color(0,0,1)):
            value = []
            for matrix in self.animation: value.append(self.paint_matrix(matrix,color1,color2))
            return value
        def paint_matrix(self, matrix,color1, color2=Color(0,0,1)):
            value = []
            if self.m == True: m = matrix.matrix
            else: m = matrix
            for i in m:
                val = []
                for j in i:
                    if j == 1: val.append(color1)
                    else: val.append(color2)
                value.append(val)
            return value
        def rotate(self, times):
            r = []
            for matrix in self.animation: r.append(self.girar_matrix(matrix,times))
            return r
        def girar_matrix(self,matrix,times):
            if self.m == True: r1 = matrix.matrix
            else: r1 = matrix
            if times >= 2:
                times -= 2
                r2 = []
                for i in range(len(r1)): r2.append(r1[7-i])
            else: r2 = r1
            if times >= 1:
                r3 = []
                for i in range(8):
                    r3b = []
                    for j in range(8): r3b.append(r2[j][i])
                    r3.append(r3b)
            else: r3 = r2
            return r3

if __name__ == "__main__":
    screen = Screen()
    time.sleep(1)
    screen.text("8·8",fg=Color(100,100,100))
    time.sleep(11)
    screen.text("R",fg=Color(255,0,0))
    time.sleep(3)
    screen.text("G",fg=Color(0,255,0))
    time.sleep(2)
    screen.text("B",fg=Color(0,0,255))
    time.sleep(2)
    screen.toogleRainbow(1)
    screen.text("&",fg=Color(0,0,0)) # $ is a WiFi icon, & is a heart, ¬ is a box, # is the full screen
    time.sleep(3)
    screen.toogleRainbow(2)
    screen.anim(screen.animation[5].paint(Color(0,0,0)))
    while True: pass