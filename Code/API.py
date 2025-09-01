from Thread import Variable,Thread,Runner
from System import read

from tuya_iot import TuyaOpenAPI, AuthType,TuyaOpenMQ,TuyaDeviceManager,TuyaHomeManager,TuyaDeviceListener,TuyaDevice,TuyaTokenInfo,TUYA_LOGGER
import logging
from colorama import Fore
import berserk
import time

class lichess_game(Runner):
    def __init__(self):
        super(lichess_game,self).__init__(None)
    def init(self):
        self.TOKEN = 'API'
        session = berserk.TokenSession(self.TOKEN)
        self.client = berserk.Client(session=session)
        self.c = 0
        response = self.client.challenges.create_ai(level=3)
        self.game_id = response['id']
        print(f"Game created, game ID: {self.game_id}")
        self.move_var = Variable([" "])
        self.thread = Thread(self.update_move)
        self.thread.start()
        for event in self.client.bots.stream_incoming_events():
            if event['type'] == 'gameStart':
                print("¡Game started!")
                break
        try:
            self.client.games.export(self.game_id)["players"]["black"]["user"]
            self.c=1
        except: pass
        print(["White","Black"][self.c])
        self.end = 0
        self.count = 0
        if self.c == 1: self.wait()
        self.count = self.c
    def update_move(self):
        m = []
        state = self.client.board.stream_game_state(self.game_id)
        for i in state: 
            try: self.move_var.write(i["moves"].split())
            except: self.move_var.write(i["state"]["moves"].split())
    def moves(self): return self.move_var.read()
    def load(self):
        self.game_state = self.client.games.export(self.game_id)
        move = self.last()
        if self.game_state['status'] != 'started':
            print("The game is ended.")
            self.end = 1
        return move
    def play(self,move):
        try:
            self.client.board.make_move(self.game_id, move)
            self.count += 1
            return 1
        except: return 0
    def wait(self):
        self.load()
        while len(self.moves()) <= self.count: time.sleep(1)
        self.count += 1
        return self.load()
    def last(self):
        moves = self.moves()
        if len(moves) >= 1 and moves != [" "]:
            move = moves[len(moves)-1]
            return move[0]+move[1], move[2]+move[3]
        else: return None

class tuyaDeviceListener(TuyaDeviceListener):
    def update_device(self, device: TuyaDevice): pass
    def add_device(self, device: TuyaDevice): pass
    def remove_device(self, device_id: str): pass

class Switch(Runner):
    def __init__(self): 
        super(Switch,self).__init__(None)
    def init(self): 
        try:
            data = read("tuya.json")
            ACCESS_ID,ACCESS_KEY,USERNAME,PASSWORD,self.DEVICE_ID,ENDPOINT= data["access_id"],data["access_key"],data["username"],data["password"],data["device_id"],data["endpoint"]
            self.openapi = TuyaOpenAPI(ENDPOINT,ACCESS_ID,ACCESS_KEY,AuthType.CUSTOM)
            self.openapi.connect(USERNAME,PASSWORD)
            openmq = TuyaOpenMQ(self.openapi)
            openmq.start()

            deviceManager = TuyaDeviceManager(self.openapi, openmq)
            TuyaHomeManager(self.openapi, openmq, deviceManager).update_device_cache()
            deviceManager.add_device_listener(tuyaDeviceListener())

            TUYA_LOGGER.setLevel(logging.WARNING)
        except Exception as e: 
            print(Fore.MAGENTA+"ERROR: "+Fore.WHITE+"Plugs disconnected")
    def set(self,switch,state):
        commands = {'commands': [{'code': 'switch_1', 'value': state}]}
        self.openapi.post('/v1.0/iot-03/devices/{}/commands'.format(self.DEVICE_ID[switch-1]), commands,)

if __name__ == "__main__":
    flag = True
    print("Preparando Switch...")
    switch=Switch()
    while True:
        input()
        flag = not flag
        switch.set(2,flag)
