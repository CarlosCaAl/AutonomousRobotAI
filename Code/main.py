import time
t = time.time()
WORKING_OFFLINE = False

from Assistant import Assistant, Fore
from Chat import ArtificialIntelligence
assistant = Assistant(50)
ai = ArtificialIntelligence()

from Control import Controller,robot, Color
from Thread import Variable,Run, Thread
import Games
from App import Window
from BT import PS4 
from Server import Server
from System import os, read

def respondRequests(val,n=-1,m=-1): # Function to run the main robot tools from APP/Assistant/PS4
    try:
        if n != -1: val = val + str(n)
        if m != -1: val = val + str(m)
    except: val += n
    #print(val)
    if True:
        valIndicador = val[0]
        val = val[1:]

        if valIndicador == "X": endVar.write(1)
        if valIndicador == "b": ps4.bind()
        if valIndicador != "t":
            if   valIndicador == 'm':
                if val == '0': robot.wheels.stop()
                if val == '1': robot.wheels.front()
                if val == '2': robot.wheels.back()
                if val == '3': robot.wheels.left()
                if val == '4': robot.wheels.right()
            elif valIndicador == 'l':
                valIndicador2 = val[0]
                val = val[1:]
                if   valIndicador2 == 'm': robot.animations.animations[int(val)]()
                elif valIndicador2 == 'c': color.write(Color(int(val[1:3],16),int(val[3:5],16),int(val[5:7],16)))
                elif valIndicador2 == 'C': color.write([Color(255,0,0),Color(255,100,0),Color(255,200,0),Color(100,255,0),Color(0,255,0),Color(0,200,255),Color(0,0,255),Color(100,0,255),Color(255,0,100),Color(150,50,0),Color(1,0,0),Color(255,255,255),Color(0,0,0)][int(val)])
            elif valIndicador == 't': control.start(int(val))
            elif valIndicador == 'S': assistant.random_song()
            elif valIndicador == 'p': robot.screen.show_hex(val)
            elif valIndicador == 's': robot.servo.angle(int(val[0]),int(val[1:5]))
            elif valIndicador == 'r': robot.screen.text(val,fg=color.read())
            elif valIndicador == 'V': assistant.volume(val[0])
            elif valIndicador == 'c':
                valIndicador2 = val[0]
                val = val[1:]
                if   valIndicador2 == 'c': robot.mail.send(body=val)
                if   valIndicador2 == 'm': assistant.bag.write(val)
                if   valIndicador2 == 's': assistant.say(val)
            elif valIndicador == 'v':
                valIndicador2 = val[0]
                val = val[1:]
                if   valIndicador2 == '1': robot.head.camera.save_record()
                if   valIndicador2 == '2': robot.head.camera.record()
            elif valIndicador == 'g': Games.Menu()
            elif valIndicador == "F": robot.head.camera.save_photo()
            elif valIndicador == "N": endVar.write(1)
            elif valIndicador == 'o':
                for i in val:
                    if i == "f": robot.wheels.front(20,1,color=color.read())
                    if i == "b": robot.wheels.back(20,1,color=color.read())
                    if i == "l": robot.wheels.left(90,1,color=color.read())
                    if i == "r": robot.wheels.right(90,1,color=color.read())
            elif valIndicador == 'e': switch.set(int(val[0]),[False,True,None][int(val[1])])
        else:
            if valIndicador == 't': control.start(int(val))
            if valIndicador == 'm': control.start(int(val)-1)

def end(): # End program
    endVar.write(1)
    robot.wheels.stop(color=color.read())
    control.thread.pause()

def start():
    global color,control,endVar,ps4,server,data,taskVar
    color = Variable(Color(0,100,200))
    control = Controller(color)
    def switch_start(): # Save time
        global switch
        from API import Switch
        switch = Switch()
    Run(switch_start)

    ps4 = PS4(respondRequests) # Start PS4 binding
    endVar = Variable(0) # If is 1, program ends
    taskVar = Variable(None) # Current autonomous task
    control.voice(assistant) # Pass assistant to control. This will allow the robot speak during a mode

    win = Variable(None)
    def window(): 
        robot.wait()
        win.write(Window(respondRequests,robot.head.camera.read))
    Run(window)
    server = None
    data = None
    if not WORKING_OFFLINE:  
        data = read("data.json")
        server = Server(cam=robot.head.camera, scr=robot.screen, voice=assistant, func=respondRequests,host=data["ip"])
        server.wait()
        server.start(endVar)
    assistant.wait()
    assistant.soundEffect("click")
    assistant.say("Program started after {} seconds. How can I help you?".format(round(time.time()-t,2)),mute=True)
    robot.wait()
    robot.wheels.color = color
    ps4.link(robot.screen) # Pass assistant to ps4. This will create an animation once the ps4 controller is binded
    Games.screen.write(robot.screen) # Pass screen to Games. In this way, games will be played on the screen

Run(start) # Run inside a thread

def chat_loop(): # Listen to the user, send data to ai and execute answer

    def auto_loop(error=None):

        def task_completed(task): taskVar.write(None)
    
        msg = taskVar.read() if error is not None else taskVar.read() + error
        distance = robot.head.ultrasonic.read()

        code = ai.auto(msg,robot.head.camera.photo_route(),distance).replace("```python","").replace("```","") # Create and answer
        
        try:
            #print(code)
            exec(code) # Run code generated by ai
        except Exception as e:
            auto_loop(f" Your last code failed and was not runned, please, fix it to run it again: {e}") # Manage errors

        time.sleep(5)

    def set_current_task(task): taskVar.write(task)
    def set_name_of_person(name): # Register someone's face
        if "unknown" not in name.lower() and "nobody" not in name.lower():
                if name not in robot.head.camera.face_recognizer.people:
                    robot.head.camera.face_recognizer.new(name,robot.head.camera.read)

    while taskVar.read() is not None: auto_loop()

    while assistant.bag.read() is None: time.sleep(0.01) # Wait until message is received
    msg = assistant.bag.read() # Extract message
    assistant.bag.write(None)

    robot.screen.anim(robot.screen.animation[6].paint(color.read()),speed=0.16) # Start loading animation (while processing answer)
    print(Fore.GREEN+" USER: "+Fore.WHITE+msg) # Print message

    # Collect data for ai
    ip = data["ip"] if data is not None else "No IP, the server is closed"
    img = robot.head.camera.read()
    distance = robot.head.ultrasonic.read()
    name,_ = robot.head.camera.face_recognizer.recognition(img,draw=True,reg=False)

    code = ai.answer(msg,robot.head.camera.photo_route(),name,ip,distance).replace("```python","").replace("```","") # Create and answer

    robot.screen.animThread.stop() # Kill thread to stop animation
    robot.screen.clean()
    
    try:
        #print(code)
        exec(code) # Run code generated by ai
    except Exception as e:
        assistant.bag.write(f"Your last code failed and was not runned, please, fix it to run it again: {e}") # Manage errors

assistant.wait() # Wait for the assistant to be started
robot.wait()
robot.head.camera.wait()
Thread(func=chat_loop,loop=True,start=True)

while True:
    time.sleep(.2)
    if endVar.read() == 1: 
        end()
        os.system("clear")
        break