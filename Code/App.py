from Thread import Runner
from System import read

import tkinter as tk
from tkinter.colorchooser import askcolor
import time
from PIL import Image, ImageTk
import cv2

class Window:
    def __init__(self,func2 = None, func3 = None, ONLINE=False):
        if ONLINE: from Client import Client
        else:  from FakeClient import Client

        # WINDOW STRUCTURE
        self.win0 = tk.Tk()
        self.win0.geometry('420x390')
        self.win0.title("RobotAPP")
        self.win0.config(bg='#111125')
        self.win0.protocol('WM_DELETE_WINDOW',self.Destroy)

        # Movement control
        self.m = self.Selection(self.mSend,'#66AAFF','#2266BB')
        self.m.NewBTN(self.win0,['Stop','Forward','Backward','Left','Right'],[120,120,120,20,220],[70,20,120,70,70],80,40,"qwsad")

        # Mode control
        self.a = self.Selection(self.tSend,'#FFAA66','#BB6622')
        self.a.NewBTN(self.win0,['Mode 1','Mode 2','Mode 3','Mode 4','Mode 5'],[320,320,320,320,320],[20,70,120,170,220],80,40,"12345")

        self.C = '#FFFFFF' # Actual colour
        self.cBTNd = [0,0]

        self.openWin = [0,0,0,0,0,0,0,0,0,0] # Windows opened
        self.win0.bind('<Escape>', self.Destroy) # Key to end the program

        # MENUS WHICH CAN BE OPENED
        tk.Button(self.win0,text='Animate',bg='#66FFAA',fg='#111125',command=self.LedWin).place(x=20,y=170,width=80,heigh=40)
        tk.Button(self.win0,text='Servo',bg='#66FFAA',fg='#111125',command=self.ServoWin).place(x=120,y=170,width=80,heigh=40)
        tk.Button(self.win0,text='Matrix',bg='#66FFAA',fg='#111125',command=self.MatrixWin).place(x=220,y=170,width=80,heigh=40)
        tk.Button(self.win0,text='Mail',bg='#66FFAA',fg='#111125',command=self.MailWin).place(x=20,y=220,width=80,heigh=40)
        tk.Button(self.win0,text='Switch',bg='#66FFAA',fg='#111125',command=self.PlugWin).place(x=120,y=220,width=80,heigh=40)
        tk.Button(self.win0,text='Chat',bg='#66FFAA',fg='#111125',command=self.TalkWin).place(x=220,y=220,width=80,heigh=40)
        tk.Button(self.win0,text='Minigames',bg='#66FFAA',fg='#111125',command=self.Minigames).place(x=20,y=270,width=80,heigh=40)
        tk.Button(self.win0,text='Video',bg='#66FFAA',fg='#111125',command=self.VideoWin).place(x=120,y=270,width=80,heigh=40)
        tk.Button(self.win0,text='Move',bg='#66FFAA',fg='#111125',command=self.MoveWin).place(x=220,y=270,width=80,heigh=40)

        tk.Button(self.win0,text='Exit',bg='#FF6666',fg='#111125',command=self.Destroy).place(x=20,y=330,width=80,heigh=40)
        self.clientIsOpen = not ONLINE
        if self.clientIsOpen: self.client = Client(self,self.showvideo,func2,func3) # Fake client for the offline mode
        else: self.Client = Client
        
        self.ip = tk.StringVar() # Online mode
        ipENT = tk.Entry(self.win0,textvariable=self.ip)
        ipENT.place(x=120,y=330,width=120,height=40)
        ipENT.bind('<Key-Return>', self.Connect)
        self.win0.bind('r', self.Reconnect)
        tk.Button(self.win0,text='Connect'  ,bg='#66FF66',fg='#111125',command=self.Connect).place(x=240,y=330,width=80,heigh=40)
        tk.Button(self.win0,text='Reconnect',bg='#6666FF',fg='#111125',command=self.Reconnect).place(x=320,y=330,width=80,heigh=40)


        self.win0.mainloop()

    def toogleVideo(self): 
        if self.clientIsOpen == 1: self.client.toogleVideo()

    def showvideo(self,image):
        if self.openWin[6]:
            imageToShow = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(imageToShow )
            img = ImageTk.PhotoImage(image=im)
            self.image.configure(image=img)
            self.image.image = img
            
    def Connect(self,n=None):
        if self.clientIsOpen == 0: 
            self.client = self.Client(self.ip.get())
        self.clientIsOpen = 1
    def Reconnect(self,n=None):
        if self.clientIsOpen == 0: 
            self.client = self.Client(read("data.json")["ip"])
        self.clientIsOpen = 1

    def Destroy(self,n=None): 
        self.win0.destroy()
        if self.clientIsOpen: 
            self.client.send("X")
        quit()

    def mSend(self,d): # send the direction of movement
        if self.clientIsOpen == 1: self.client.send('m'+str(d))
    def tSend(self,d): # send the mode chosen (in case of path mode, opens a new window)
        if d != 4:
            if self.clientIsOpen == 1: self.client.send('t'+str(d))
        else: self.PathWin()

    def PathWin(self): # Choose a path for the robot to follow
        if self.openWin[8] == 0: self.win9 = tk.Toplevel()
        self.openWin[8] = 1
        self.win9.bind('<Escape>', self.Destroy9)
        self.win9.bind('<Key-Return>', self.SaveM)
        self.win9.geometry('120x280')
        self.win9.title("Choose a route")
        self.win9.config(bg='#111125')
        self.win9.protocol('WM_DELETE_WINDOW',self.Destroy9)
        self.a = self.Selection(self.SavePath,'#FFAA66','#BB6622')
        self.a.NewBTN(self.win9,['Route 1','Route 2','Route 3','Route 4','Route 5'],[20,20,20,20,20],[20,70,120,170,220],80,40,"12345")
    def Destroy9(self,n=None): 
        self.win9.destroy()
        self.openWin[8] = 0
    def SavePath(self,n=None): 
        if self.clientIsOpen:
            self.client.send("t"+str(4+n))
        else: ("t"+str(4+n))
        self.Destroy9()

    def ServoWin(self): # Control the servo angles
        if self.clientIsOpen == 1:
            if self.openWin[0] == 0: self.win1 = tk.Toplevel()
            self.openWin[0] = 1
            self.win1.bind('<Escape>', self.Destroy1)
            self.win1.bind('<Key-Return>', self.SaveS)
            self.win1.geometry('590x230')
            self.win1.title("Servo")
            self.win1.config(bg='#111125')
            self.win1.protocol('WM_DELETE_WINDOW',self.Destroy1)
            self.Scales = [self.ServoScale(self.win1,'#AA66FF',20 ,20 ,0,self.client),self.ServoScale(self.win1,'#AA66FF',20 ,70 ,1,self.client),self.ServoScale(self.win1,'#66FFAA',210,20 ,2,self.client),self.ServoScale(self.win1,'#66FFAA',210,70 ,3,self.client),self.ServoScale(self.win1,'#66FFAA',210,120,4,self.client),self.ServoScale(self.win1,'#66FFAA',210,170,5,self.client),self.ServoScale(self.win1,'#66AAFF',400,20 ,6,self.client),self.ServoScale(self.win1,'#66AAFF',400,70 ,7,self.client),self.ServoScale(self.win1,'#66AAFF',400,120,8,self.client),self.ServoScale(self.win1,'#66AAFF',400,170,9,self.client)]
            tk.Button(self.win1,text='Save' ,bg='#66FF66',fg='#111125',command=self.SaveS).place(x=110,y=170,width=80,heigh=40)
            tk.Button(self.win1,text='Exit',bg='#FF6666',fg='#111125',command=self.Destroy1).place(x=20 ,y=170,width=80,heigh=40)
    def Destroy1(self,n=None): 
        self.win1.destroy()
        self.openWin[0] = 0
    def SaveS(self,n=None):
        for Scale in self.Scales:
            self.client.send('s{}{}   '.format(Scale.index,Scale.val.get()))
            time.sleep(0.5)
    class ServoScale: # Scale to choose the angle of a motor
        def __init__(self,win,bg,x,y,index,client):
            self.val = tk.IntVar()
            self.index = index
            self.client = client
            self.val.set(90)
            tk.Label(win,text='Servo {}'.format(index),bg=bg,fg='#111125').place(x=x,y=y ,width=80,heigh=40)
            tk.Scale(win,fg='#111125',bg=bg,from_=0,to=180,variable=self.val,command=self.func,orient=tk.HORIZONTAL).place(x=x+90,y=y ,width=80,heigh=40)
        def func(self,n): pass
            
    def MatrixWin(self): # Menu to edit the matrix output
        if self.openWin[1] == 0: self.win2 = tk.Toplevel()
        self.openWin[1] = 1
        self.win2.bind('<Escape>', self.Destroy2)
        self.win2.bind('<Key-Return>', self.SaveM)
        self.win2.geometry('314x274')
        self.win2.title("Matrix")
        self.win2.config(bg='#111125')
        self.win2.protocol('WM_DELETE_WINDOW',self.Destroy2)
        self.cBTNd[1] = 1
        self.btnC2 = tk.Button(self.win2,text='Color',bg=self.C,fg='#111125',command=self.cSet)
        self.btnC2.place(x=214,y=20,width=80,heigh=40)
        self.p = []
        for j in range(8):
            for i in range(8): self.p.append(self.Pixel(self.win2,20+i*22,20+j*22,self.selectedColor))
        tk.Button(self.win2,text='Eraser',bg='#111125',fg='#FFFFFF',command=self.Eraser  ).place(x=214 ,y=80,width=80,heigh=40)
        tk.Button(self.win2,text='Fill',bg='#FFFFFF',fg='#111125',command=self.Fill    ).place(x=214 ,y=200,width=80,heigh=40)
        tk.Button(self.win2,text='Rainbow',bg='#FF66AA',fg='#111125',command=self.Rainbow ).place(x=214 ,y=140,width=80,heigh=40)
        tk.Button(self.win2,text='Save' ,bg='#66FF66',fg='#111125',command=self.SaveM   ).place(x=20 ,y=214,width=77,heigh=40)
        tk.Button(self.win2,text='Exit'   ,bg='#FF6666',fg='#111125',command=self.Destroy2).place(x=117,y=214,width=77,heigh=40)
    def SaveM(self,n=None):
        val = []
        sendVal = 'p'
        if self.clientIsOpen == 1:
            for i in range(8):
                valr = []
                for j in range(8):
                    valr.append(self.p[8*i+j].State())
                    sendVal += self.p[8*i+j].State()
                val.append(valr)
            self.client.send(sendVal)
    def Eraser(self):
        self.C = '#000001'
        if self.cBTNd[0] == 1: self.btnC1.config(bg=self.C)
        if self.cBTNd[1] == 1: self.btnC2.config(bg=self.C)
    def Rainbow(self):
        self.C = '#000000' # The program replaces #000000 by rainbow colour
        if self.clientIsOpen == 1: self.client.send('lc'+self.C)
        if self.cBTNd[0] == 1: self.btnC1.config(bg=self.C)
        if self.cBTNd[1] == 1: self.btnC2.config(bg=self.C)
    def Fill(self):
        for i in range(64): self.p[i].Toogle()
    def Destroy2(self,n=None):
        self.win2.destroy()
        self.cBTNd[1] = 0
        self.openWin[1] = 0
    class Pixel: # 1 of the 64 buttons which change their colour for the selected one when clicked
        def __init__(self,win,x,y,colorFunc, w=20, h=20,n=None):
            self.c = '#000001'
            if n is not None: self.c = '#FF66AA'
            self.func = colorFunc
            self.p = tk.Button(win,text='',bg=self.c,command=self.Toogle)
            if n is not None: self.p.config(text="OFF")
            self.p.place(x=x,y=y,width=w,heigh=h)
            self.n = n
        def Toogle(self):
            if self.n is not None:
                if self.c == '#FF66AA': 
                    self.p.config(bg="#66FFAA",text="ON")
                    self.n(1)
                    self.c="#66FFAA"
                else: 
                    self.p.config(bg='#FF66AA',text="OFF")
                    self.n(0)
                    self.c="#FF66AA"
            else: 
                self.c = self.func()
                if self.c != '#000000': self.p.config(bg=self.c)
                else: self.p.config(bg='#FF00AA')
        def State(self): return self.c

    def LedWin(self,n=None): # Several commands 
        if self.openWin[2] == 0: self.win3 = tk.Toplevel()
        time.sleep(.2)
        self.openWin[2] = 1
        self.win3.bind('<Escape>', self.Destroy3)
        self.win3.geometry('220x300')
        self.win3.title("Animations")
        self.win3.config(bg='#111125')
        self.win3.protocol('WM_DELETE_WINDOW',self.Destroy3)
        self.cBTNd[0] = 1
        self.msg = tk.StringVar() # Send a text to the robot to display it on the screen
        msgENT = tk.Entry(self.win3,textvariable=self.msg)
        msgENT.place(x=20,y=180,width=100,height=40)
        msgENT.bind('<Key-Return>', self.SendMessage)
        tk.Button(self.win3,text='Send'  ,bg='#66FF66',fg='#111125',command=self.SendMessage).place(x=120,y=180,width=80,heigh=40)
        self.btnC1 = tk.Button(self.win3,text='Color',bg=self.C,fg='#111125',command=self.cSet) # Change chosen colour
        self.btnC1.place(x=20,y=20,width=180,heigh=40)
        self.c = self.Selection(self.cMode,'#FF66AA','#BB2266')
        self.c.NewBTN(self.win3,['Anim 1','Anim 2','Anim 3','Anim 4'],[20,20,120,120],[80,130,80,130],80,40,"1234")
        tk.Button(self.win3,text='Exit',bg='#FF6666',fg='#111125',command=self.Destroy3).place(x=20,y=240,width=80,heigh=40)
    def cSet(self):
        c = askcolor(color=self.C,title='COLOR')
        if self.clientIsOpen == 1: self.client.send('lc'+c[1])
        else: ("Debes conectarte al servidor antes de enviar cualquier orden\n")
        self.C = c[1]
        if self.cBTNd[0] == 1: self.btnC1.config(bg=c[1])
        if self.cBTNd[1] == 1: self.btnC2.config(bg=c[1])
    def cMode(self,m):
        if self.clientIsOpen == 1: self.client.send('lm'+str(m))
        else: ("Debes conectarte al servidor antes de enviar cualquier orden\n")
    def selectedColor(self): return self.C
    def SendMessage(self,n=None):
        if self.clientIsOpen == 1:
            self.client.send("r"+self.msg.get())
        else: (self.msg.get())
    def Destroy3(self,n=None):
        self.win3.destroy()
        self.cBTNd[0] = 0
        self.openWin[2] = 0

    def MailWin(self,n=None): # Window to send emails
        if self.openWin[3] == 0: self.win4 = tk.Toplevel()
        time.sleep(.2)
        self.openWin[3] = 1
        self.win4.bind('<Escape>', self.Destroy4)
        self.win4.geometry('230x130')
        self.win4.title("Mail")
        self.win4.config(bg='#111125')
        self.win4.protocol('WM_DELETE_WINDOW',self.Destroy4)
        tk.Label(self.win4,text='Text to send',bg='#FF66AA').place(x=20,y=20,width=100,height=40)
        self.msg2 = tk.StringVar()
        msgENT2 = tk.Entry(self.win4,textvariable=self.msg2)
        msgENT2.place(x=20,y=70,width=110,height=40)
        msgENT2.bind('<Key-Return>', self.SendMessage2)
        tk.Button(self.win4,text='Send'  ,bg='#66FF66',fg='#111125',command=self.SendMessage2).place(x=130,y=70,width=80,heigh=40)
        tk.Button(self.win4,text='Exit',bg='#FF6666',fg='#111125',command=self.Destroy4).place(x=130,y=20,width=80,heigh=40)
    def Destroy4(self,n=None):
        self.win4.destroy()
        self.openWin[3] = 0
    def SendMessage2(self,n=None):
        if self.clientIsOpen == 1:
            self.client.send("cc"+self.msg2.get())
        else: (self.msg2.get())
    def TalkWin(self,n=None): # Window to chat with the chatbot through text
        if self.openWin[4] == 0: self.win5 = tk.Toplevel()
        time.sleep(.2)
        self.openWin[4] = 1
        self.win5.bind('<Escape>', self.Destroy5)
        self.win5.geometry('230x240')
        self.win5.title("Chat")
        self.win5.config(bg='#111125')
        self.win5.protocol('WM_DELETE_WINDOW',self.Destroy5)
        tk.Label(self.win5,text='Text to listen',bg='#FF66AA').place(x=20,y=20,width=100,height=40)
        self.msg3 = tk.StringVar()
        msgENT3 = tk.Entry(self.win5,textvariable=self.msg3)
        msgENT3.place(x=20,y=70,width=110,height=40)
        msgENT3.bind('<Key-Return>', self.SendMessage3)
        tk.Button(self.win5,text='Send'  ,bg='#66FF66',fg='#111125',command=self.SendMessage3).place(x=130,y=70,width=80,heigh=40)
        tk.Label(self.win5,text='Text to say',bg='#FF66AA').place(x=20,y=130,width=190,height=40)
        self.msg4 = tk.StringVar()
        msgENT4 = tk.Entry(self.win5,textvariable=self.msg4)
        msgENT4.place(x=20,y=180,width=110,height=40)
        msgENT4.bind('<Key-Return>', self.SendMessage4)
        tk.Button(self.win5,text='Send'  ,bg='#66FF66',fg='#111125',command=self.SendMessage4).place(x=130,y=180,width=80,heigh=40)
        tk.Button(self.win5,text='Exit',bg='#FF6666',fg='#111125',command=self.Destroy5).place(x=130,y=20,width=80,heigh=40)
    def Destroy5(self,n=None):
        self.win5.destroy()
        self.openWin[4] = 0
    def SendMessage3(self,n=None):
        if self.clientIsOpen == 1:
            self.client.send("cm"+self.msg3.get())
        else: (self.msg3.get())
    def SendMessage4(self,n=None):
        if self.clientIsOpen == 1:
            self.client.send("cs"+self.msg4.get())
        else: (self.msg4.get())
    def PlugWin(self,n=None): # Window to modify the state of the tuya plugs
        if self.openWin[5] == 0: self.win6 = tk.Toplevel()
        time.sleep(.2)
        self.openWin[5] = 1
        self.win6.bind('<Escape>', self.Destroy6)
        self.win6.geometry('180x200')
        self.win6.title("Plugs")
        self.win6.config(bg='#111125')
        self.win6.protocol('WM_DELETE_WINDOW',self.Destroy6)
        tk.Label(self.win6,text='Plug 1',bg='#66AAFF').place(x=20,y=20,width=80,height=40)
        tk.Label(self.win6,text='Plug 2',bg='#66AAFF').place(x=20,y=80,width=80,height=40)
        self.Pixel(self.win6,120,20,self.selectedColor,40,40,self.Plug1)
        self.Pixel(self.win6,120,80,self.selectedColor,40,40,self.Plug2)
        tk.Button(self.win6,text='Exit',bg='#FF6666',fg='#111125',command=self.Destroy6).place(x=20,y=140,width=80,heigh=40)
    def Plug1(self,v):
        if self.clientIsOpen == 1: self.client.send("e1"+str(v))
        else: ("e1"+str(v))
    def Plug2(self,v):
        if self.clientIsOpen == 1: self.client.send("e2"+str(v))
        else: ("e2"+str(v))
    def Destroy6(self,n=None):
        self.win6.destroy()
        self.openWin[5] = 0
    def Minigames(self,n=None): # Run the minigames
        if self.clientIsOpen == 1:
            self.client.send("g")
        else: pass
    def VideoWin(self,n=None): # Window to receive the video and take photographs
        if self.openWin[6] == 0: self.win7 = tk.Toplevel()
        time.sleep(.2)
        self.openWin[6] = 1
        self.win7.bind('<Escape>', self.Destroy7)
        self.win7.geometry('680x580')
        self.win7.title("Video")
        self.win7.config(bg='#111125')
        self.win7.protocol('WM_DELETE_WINDOW',self.Destroy7)
        self.image = tk.Label(self.win7)
        tk.Button(self.win7,text='Exit'  ,bg='#FF6666',fg='#111125',command=self.Destroy7).place(x=580,y=20,width=80,heigh=40)
        tk.Button(self.win7,text='Photo'   ,bg='#AAFF66',fg='#111125',command=self.Photo).place(x=480,y=20,width=80,heigh=40)
        tk.Button(self.win7,text='Record' ,bg='#FF66AA',fg='#111125',command=self.Record).place(x=380,y=20,width=80,heigh=40)
        tk.Label(self.win7,text='Robot camera',bg="#66AAFF",fg='#111125').place(x=20,y=20 ,width=340,heigh=40)
        self.image.place(x=20,y=80,width=640,height=480)
    def Photo(self): self.client.send("v1")
    def Record(self): self.client.send("v2")
    def Destroy7(self,n=None):
        self.win7.destroy()
        self.openWin[6] = 0
    def MoveWin(self,n=None): # Window to program blocks indicating the desired movement of the robot
        if self.openWin[7] == 0: self.win8 = tk.Toplevel()
        time.sleep(.2)
        self.openWin[7] = 1
        self.win8.bind('<Escape>', self.Destroy8)
        self.win8.geometry('770x150')
        self.win8.title("Movement")
        self.win8.config(bg='#111125')
        self.win8.protocol('WM_DELETE_WINDOW',self.Destroy8)
        self.commands = ""
        self.commandslen = 0
        self.commandblocks = []
        self.commandarea = tk.Label(self.win8,text='',bg="#FFFFFF",fg="#111125")
        self.commandarea.place(x=20,y=80,width=730,height=50)
        self.win8.bind('<Key-Return>', self.SaveCommand)
        self.win8.bind('<Control-z>', self.CleanCommand)
        self.win8.bind('w', self.CommandFront)
        self.win8.bind('s', self.CommandBack)
        self.win8.bind('d', self.CommandRight)
        self.win8.bind('a', self.CommandLeft)
        tk.Button(self.win8,text='Front(20)',bg='#FF66AA',fg='#111125',command=self.CommandFront ).place(x=20 ,y=20,width=80,heigh=40)
        tk.Button(self.win8,text='Back(20)',bg='#66FFAA',fg='#111125',command=self.CommandBack ).place(x=120 ,y=20,width=80,heigh=40)
        tk.Button(self.win8,text='Right(90)',bg='#AAFF66',fg='#111125',command=self.CommandRight ).place(x=220 ,y=20,width=80,heigh=40)
        tk.Button(self.win8,text='Left(90)',bg='#66AAFF',fg='#111125',command=self.CommandLeft ).place(x=320 ,y=20,width=80,heigh=40)
        tk.Button(self.win8,text='Save' ,bg='#66FF66',fg='#111125',command=self.SaveCommand   ).place(x=470 ,y=20,width=80,heigh=40)
        tk.Button(self.win8,text='Exit'   ,bg='#FF6666',fg='#111125',command=self.Destroy8).place(x=570,y=20,width=80,heigh=40)
        tk.Button(self.win8,text='Undo'   ,bg='#6666FF',fg='#111125',command=self.CleanCommand).place(x=670,y=20,width=80,heigh=40)
    def Destroy8(self,n=None):
        self.win8.destroy()
        self.openWin[7] = 0
    def CommandFront(self,n=None):
        c = 0
        for i in self.commands:
            if i == "f": c += 1
            else: c = 0
        self.commands += "f"
        if c == 0: 
            self.commandslen += 1
            self.commandblocks.append(tk.Label(self.win8,text='Front(20)',fg="#FF66AA",bg="#111125"))
            self.commandplace()
        else: self.commandblocks[len(self.commandblocks)-1].config(text="Front({})".format(20+c*20))
    def CommandBack(self,n=None):
        c = 0
        for i in self.commands:
            if i == "b": c += 1
            else: c = 0
        self.commands += "b"
        if c == 0: 
            self.commandslen += 1
            self.commandblocks.append(tk.Label(self.win8,text='Back(20)',fg='#66FFAA',bg='#111125'))
            self.commandplace()
        else: self.commandblocks[len(self.commandblocks)-1].config(text="Back({})".format(20+c*20))
    def CommandLeft(self,n=None):
        c = 0
        for i in self.commands:
            if i == "l": c += 1
            else: c = 0
        self.commands += "l"
        if c == 0: 
            self.commandslen += 1
            self.commandblocks.append(tk.Label(self.win8,text='Left(90)',fg='#66AAFF',bg='#111125'))
            self.commandplace()
        else: self.commandblocks[len(self.commandblocks)-1].config(text="Left({})".format(90+c*90))
    def CommandRight(self,n=None):
        c = 0
        for i in self.commands:
            if i == "r": c += 1
            else: c = 0
        self.commands += "r"
        if c == 0: 
            self.commandslen += 1
            self.commandblocks.append(tk.Label(self.win8,text='Right(90)',fg='#AAFF66',bg='#111125'))
            self.commandplace()
        else: self.commandblocks[len(self.commandblocks)-1].config(text="Right({})".format(90+c*90))
    def SaveCommand(self,n=None):
        if self.clientIsOpen: self.client.send("o"+self.commands)
        else: ("o"+self.commands)
    def CleanCommand(self,n=None):
        try:
            c = 0
            l = "a"
            for i in self.commands:
                if i == l: c += 1
                else: 
                    l = i
                    c = 0
            copy = ""
            for i in range(len(self.commands)-1): copy += self.commands[i]
            self.commands = copy
            if c == 0: 
                self.commandblocks[len(self.commandblocks)-1].destroy()
                self.commandblocks.pop(self.commandslen-1)
                self.commandslen -= 1
                self.commandplace()
            elif l == "f" : self.commandblocks[self.commandslen-1].config(text="Front({})".format(20*c))
            elif l == "b" : self.commandblocks[self.commandslen-1].config(text="Back({})".format(20*c))
            elif l == "r" : self.commandblocks[self.commandslen-1].config(text="Right({})".format(90*c))
            elif l == "l" : self.commandblocks[self.commandslen-1].config(text="Left({})".format(90*c))
        except: pass
    def commandplace(self):
        h = self.commandslen
        c = 0
        while h > 9: 
            h-=9
            c+=1
        self.commandarea.place(x=20,y=80,width=730,height=50+45*c)
        self.win8.geometry('770x{}'.format(150+45*c))
        self.commandblocks[self.commandslen-1].place(x=25-80+h*80,y=85+45*c,width=80,height=40)
        
    class Selection: # create a menu from which 5 options are available
        def __init__(self,func,color,color2):
            self.state = 0
            self.BTN = []
            self.read = []
            self.func = func
            self.color = color
            self.color2 = color2
            self.BTNf = [self.BTN0,self.BTN1,self.BTN2,self.BTN3,self.BTN4]
        def NewBTN(self,win,txt,x,y,w,h,l):
            for i in range(len(txt)):
                self.read.append(tk.IntVar())
                self.read[i].set(0)
                self.BTN.append(tk.Button(win,text=txt[i],bg=self.color,fg='#111125',command=self.BTNf[i]))
                self.BTN[i].place(x=x[i],y=y[i],width=w,heigh=h)
                win.bind(l[i],self.BTNf[i])
        def BTN0(self,n=None): self.Show(0)
        def BTN1(self,n=None): self.Show(1)
        def BTN2(self,n=None): self.Show(2)
        def BTN3(self,n=None): self.Show(3)
        def BTN4(self,n=None): self.Show(4)
        def Show(self,state):
            self.state = state
            for i in range(1,len(self.BTN)):
                if i == self.state: self.BTN[i].config(bg=self.color2)
                else: self.BTN[i].config(bg=self.color)
            n = self.func(self.state) 

    def AddImage(self,win,path,x,y,w,h): # Insert an image in the window
        img = tk.PhotoImage(file=path)
        lbl = tk.Label(win)
        lbl.place(x=x,y=y,width=w,height=h)
        lbl.configure(image=img)
        lbl.image = img

if __name__ == "__main__":
    Window(ONLINE = True)