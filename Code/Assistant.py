from Thread import Thread,Runner,Run,Variable
from System import os, read, PATH

from vosk import Model,KaldiRecognizer
from gtts import gTTS as tts
from mutagen.mp3 import MP3
import pyaudio
import time
import vlc
from colorama import Fore
import sys
import contextlib

@contextlib.contextmanager
def silence(): # Stop Assistant throwing messages into the terminal
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try: yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

class Assistant(Runner):
    def __init__(self,volume):
        super(Assistant,self).__init__([volume])
    def init(self,volume):
        Run(self.recog) # Run in a thread to save time (the objective is to start the main program the fastest)
        Run(self.speak)
        self.VOLUME = volume
        self.conditions,self.listening,self.queue,self.active,self.talking = [],0,0,1,0
        self.started = -2
        self.p = None
        self.screen = None
        self.last = ""
    def recog(self):
        with silence(): 
            self.recognizer = KaldiRecognizer(Model(PATH + 'audio/vosk-model-small-es-0.42'),16000) # This vosk model understands spanish
            self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=8192)
            self.stream.start_stream()
        self.bag = Variable(None)
        self.thread = Thread(func=self.listen_until_call,loop=True,start=True)
        self.started += 1
    def speak(self): 
        self.ip = read("bt.json")["speaker"] # BT speaker
        os.system("sudo bluetoothctl connect {}  > /dev/null".format(self.ip))
        self.instance = vlc.Instance()
        self.ruta = PATH+'audio/Audio_out.mp3'
        self.effectFolder = PATH+'audio/effects/'
        self.musicFolder = PATH+'audio/music/'
        self.started += 1
        
    def say(self,msg,mute=False): # Transform text into audio and play it
        if msg != " ":
            if not mute:
                self.queue += 1
                Thread(func=self.sayFunc,param=(msg,self.queue)).start()
            else: print(Fore.CYAN+"ROBOT: " +Fore.WHITE+ msg)
    def sayFunc(self,msg,queue):
        while queue != self.active: pass # Wait for its turn in the queue
        self.talking = 1
        print(Fore.CYAN+"ROBOT: " +Fore.WHITE+ msg)
        tts(msg, lang = 'es-us').save(self.ruta) # This case works for spanish
        time.sleep(.1)
        m = self.instance.media_new(self.ruta)
        self.p = self.instance.media_player_new()
        self.p.set_media(m)
        vlc.libvlc_audio_set_volume(self.p,self.VOLUME)
        self.p.play()
        time.sleep(int(MP3(self.ruta).info.length))
        self.loading = 0
        self.last = msg
        self.talking = 0
        self.active += 1 # It is the turn for the following message queued
    def song(self,song): # play a song and dance
        self.silence()
        #self.control.dance(self.musicFolder+song,self.music)
    def soundEffect(self,msg): # play a sound effect
        self.queue += 1
        Thread(func=self.soundEffectFunc,param=(self.effectFolder+msg,self.queue)).start()
    def music(self,msg,r=0): # play music
        self.queue += 1
        if r == 0: msg = self.musicFolder+msg
        Thread(func=self.soundEffectFunc,param=(msg,self.queue)).start()
    def soundEffectFunc(self,msg,queue):
        while queue != self.active: pass
        self.talking = 1
        self.singing = 1
        self.p = self.instance.media_player_new()
        self.p.set_media(self.instance.media_new(msg+'.mp3'))
        vlc.libvlc_audio_set_volume(self.p,self.VOLUME)
        self.p.play()
        time.sleep(int(MP3(msg+'.mp3').info.length))
        self.talking = 0
        self.active += 1
        self.singing = 0
    def silence(self):  # stop any audio
        if self.p is not None: 
            self.p.stop()
            self.talking = 0
            if self.singing: self.control.stopMusic()
            self.singing = 0
    def anounce(self,msg1,msg2): # say a message and show it on the screen
        self.screen.text(msg2+' ',fg=self.color.read())
        self.say(msg1)

    def listen(self): # LISTEN TO THE USER
        r = ""
        while self.talking == 1:
            time.sleep(.1)
        while r == "":
            self.listening = 0
            if self.recognizer.AcceptWaveform(self.stream.read(4096)): r = self.recognizer.Result()[14:-3]
            if r in self.last: r = "" 
        return r
    def listen_until_call(self): # Listen until the robot is called (robot is the hotword)
        while self.talking == 1: pass
        msg = self.listen()
        if "robot" in msg.lower(): self.bag.write(msg)
    def volume(self,n):
        self.VOLUME += 10 * n
        if self.VOLUME < 0: self.VOLUME = 0
        if self.VOLUME > 100: self.VOLUME = 100

