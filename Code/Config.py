from System import *

import time
import math
import json


def regresion(x,y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xx = sum(xi ** 2 for xi in x)
    sum_yy = sum(yi ** 2 for yi in y)
    sum_xy = sum(y[i]*x[i] for i in range(n))
    try: a = (n*sum_xy-sum_x*sum_y)/(n*sum_xx-sum_x**2)
    except: a=0
    b = (sum_y-a*sum_x)/n
    try: r = (n*sum_xy-sum_x*sum_y)/((n*sum_xx-sum_x**2)*(n*sum_yy-sum_y**2))**0.5
    except: r=0
    return a,b,r


def rotate(data,n):
    x = []
    y = []
    for k in range(3):
        print(xa,end=" ")
        if n: motor.right()
        else: motor.left()
        t0 = time.time()
        input(f"Click [Enter] once the robot turns around {6+k} times. ")
        y += [time.time()-t0]
        motor.stop()
        x += [(12+2*k)*math.pi]
    a,b,r = regresion(x,y)
    print(a,b,r)
    data[f"w{n+1}"] = [a,b,r]
    return data

a = input("Welcome to the configuration of the robot. What do you wish to do: Movement calibration [1] or Register an account and your data [2]\n   >>>   ")
if "2" in a:
    route = "data.json"
    data = {"ip":"","mail":"","pass":"","recv":"","api":""}
    os.system("clear")
    os.system("ifconfig")
    print("\n Write down your IP direction")
    data["ip"] = "192.168." + input(" >>> 192.168.")
    os.system("clear")
    print("\n Write down your email")
    data["mail"] = input(" >>> ")
    print("\n Write down your password (or google app key)")
    data["pass"] = input(" >>> ")
    print("\n Write down the email you wish to write to")
    data["recv"] = input(" >>> ")
    print("\n Copy your groq api")
    data["api"] = input(" >>> ")
    print("\n Process completed !!!")
    write(data,route)
else:
    import RPi.GPIO as Pin
    from Motor import Motor
    from Ultrasonic import Ultrasonic
    from Servo import Servo
    myservo = Servo()
    Pin.setwarnings(False)
    Pin.setmode(Pin.BCM)
    motor = Motor(Pin)
    ultrasonic = Ultrasonic(Pin)
    time.sleep(1)
    myservo.angle(0,98)
    data = read("speed.json")
    motor.left(3.14159265)
    motor.stop()
    while "4" not in a:
        a = input("\n Which movement do you use to measure? \n [1] Front and back \n [2] Right \n [3] Left \n [4] Exit\n   >>>   ")
        if "1" in a:
            x1 = []
            x2 = []
            y = []
            for k in range(3):
                for j in range(7):
                    xa = ultrasonic.read()
                    print(xa,end=" ")
                    motor.back()
                    time.sleep(j/2)
                    motor.stop()
                    xb = ultrasonic.read()
                    print(xb,end=" ")
                    x1 += [xb-xa]
                    print(xb-xa,end=" ")
                    motor.front()
                    time.sleep(j/2)
                    motor.stop()
                    xc = ultrasonic.read()
                    x2 += [xb-xc]
                    print(xc,end=" ")
                    print(xb-xc)
                    y += [j/2]
            a1,b1,r1 = regresion(x1,y)
            a2,b2,r2 = regresion(x2,y)
            data["v1"] = [a1,b1,r1]
            data["v2"] = [a2,b2,r2]
        else:
            if "4" not in a:
                rotate(data,"2" in a)
    write(data, "speed.json")
