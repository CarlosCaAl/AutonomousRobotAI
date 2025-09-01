# -*- coding: utf-8 -*-

import math 
import cv2 as cv
import numpy as np
import time

class Trigonometry:
    def  Sin(self,x): return  math.sin(x*math.pi/180) 
    def  Cos(self,x): return  math.cos(x*math.pi/180)
    def Asin(self,x): return math.asin(x)*180/math.pi
    def Atan(self,x): return math.atan(x)*180/math.pi
    def Acos(self,x): 
        if x >=  1: x = 1
        if x <= -1: x = .1
        return math.acos(x)*180/math.pi
    def rote(self,v,t): 
        v += t
        if v > 2: v -= 3
        return v
    def sqrt(self,x): return math.sqrt(x)
    def op(self,v): return self.rote(v,1),self.rote(v,2)
    def sq(self,n): return n*n
    def triangle(self,side1,side2,side3,angle1,angle2,angle3): # Solve any triangle (existing or not)
        values = [side1,side2,side3,angle1,angle2,angle3]
        missing = None
        for i in range(6):
            if values[i] == -182: values[i],missing = -181,i
        real = 1
        while values[missing] == -181:
            for i in range(3):
                if values[i] == 0: 
                    real=0
                    values[i+3] = 0
                    n1,n2 = self.op(i)
                    values[n1+3],values[n2+3] = 90,90
                    if values[n1] == -181: values[n1] = values[n2]
                    if values[n2] == -181: values[n2] = values[n1]
                if values[i+3] == 0:
                    real=0
                    n1,n2 = self.op(i)
                    if values[n1+3] == 180: values[n2+3] == 0
                    if values[n2+3] == 180: values[n1+3] == 0
            if real:
                for i in range(3):
                    n1,n2 = self.op(i)
                    if values[i+3] == -181 and values[n1+3] != -181 and values[n2+3] != -181: values[i+3] = 180 - (values[n1+3] + values[n2+3])
                    if values[i] == -181 and values[i+3] != -181 and values[n1] != -181 and values[n2] != -181: values[i] = math.sqrt(math.pow(values[n1],2) + math.pow(values[n2],2) - 2 * values[n1] * values[n2] * self.Cos(values[i+3]))
                    if values[i+3] == -181 and values[0] != -181 and values[1] != -181 and values[2] != -181 and n1 != 0 and n2 != 0: values[i+3] = self.Acos((pow(values[i],2) - pow(values[n1],2) - pow(values[n2],2)) / (-2 * values[n1] * values[n2]))
                    for j in range(3):
                        n = self.rote(i,j)
                        if values[i] == -181 and values[i+3] != -181 and values[n] != -181 and values[n+3] != -181: values[i] = values[n] * self.Sin(values[i+3]) / self.Sin(values[n+3])
                        if values[i+3] == -181 and values[i] != -181 and values[n] != -181 and values[n+3] != -181: values[i+3] = self.Asin(self.Sin(values[n+3]) * values[i] / values[n])
        return values[missing]

t = Trigonometry()

class Angle: # Float between -180 and 180
    def __init__(self,val=0): self.val = val
    def rotate(self, angle):
        self.val += angle
        if self.val >  180: self.val -= 360
        if self.val < -180: self.val += 360
    def value(self): return self.val

class Coords: # Cartesian system
    class Point:
        def __init__(self,c,link=[]): # objects linked depend on this object
            self.x,self.y,self.z = c
            self.l,self.t,self.p = link,0,c
        def show(self,img,show = True): # Show point on an image
            for i in self.l: i.show(img)
            if show: cv.circle(img,(int(self.x),int(self.y)),6,(0,200,200), -1)
        def copy(self): return Coords().Point((self.x,self.y,self.z)) # Clone this object
        def supercopy(self): # Clone this object and the items linked to it
            l = []
            for i in self.l: l.append(i.supercopy())
            return Coords().Point((self.x,self.y,self.z),l)
        def move(self,c): # Add coordinates
            self.x += c[0]
            self.y += c[1]
            self.z += c[2]
            self.p = (self.x,self.y,self.z)
            for i in self.l: i.move(c)
        def change(self,c): # Change coordinates
            self.x,self.y,self.z = c
            self.p = c
            for i in self.l: i.change(c)
        def val(self): return self.p # returns (x,y,z)
    def Distance(self,p1,p2): return abs(t.triangle(t.triangle(p2.x-p1.x,p2.y-p1.y,-182,-181,-181,90),p2.z-p1.z,-182,-181,-181,90)) # distance between two points
    class Vector:
        def __init__(self,p): # A vector is defined by to points A,B
            self.A,self.B = p
            self.calc()
            self.t,self.a = 1,Angle()
        def show(self,img):
            for i in self.A.l: i.show(img)
            self.B.show(img,False)
            cv.line(img,(int(self.A.x),int(self.A.y)),(int(self.B.x),int(self.B.y)),(200,0,200),8)
        def move(self,c):
            self.A.move(c)
            self.B.move(c)
        def change(self,c):
            self.A.change(c)
            self.B.change(c)
        def copy(self): return Coords().Vector((self.A.copy(),self.B.copy()))
        def supercopy(self): return Coords().Vector((self.A.supercopy(),self.B.supercopy()))
        def calc(self):
            self.x,self.y,self.z = self.B.x - self.A.x,self.B.y - self.A.y,self.B.z - self.A.z
            self.xz = t.triangle(-182,self.x,self.z,90,-181,-181)
            b,c =  t.triangle(-181,self.z,self.x,90,-182,-181),t.triangle(-181,self.y,self.xz,90,-182,-181)
            if self.z < 0: b = -b
            if self.x < 0: b = 180-b
            if self.y < 0: c = -c
            return b,c
        def rotateFunc(self,a,P,r=0):
            b,c = self.calc()
            ux,uy,uz = -self.A.x, -self.A.y, -self.A.z
            P1 = P.copy()
            P1.move((ux,uy,uz))
            P2 = self.rotation_matrix(-b,0,self.rotation_matrix(-c,1,self.rotation_matrix(a,-1,self.rotation_matrix(c,1,self.rotation_matrix(b,0,P1)))))
            P3 = P2.copy()
            P3.move((-ux,-uy,-uz))
            P.change((P3.x,P3.y,P3.z))
            if r: return P3
        def rotate(self,a,P=None): # Rotate this vector and objects linked to it an angle (a) 
            if P is None: 
                self.a.rotate(a)
                for i in self.A.l: self.rotate(a,i)
            else:
                if P.t == 0: self.rotateFunc(a,P)
                if P.t == 1:
                    self.rotateFunc(a,P.A)
                    self.rotateFunc(a,P.B)
                if P.t == 2:
                    for i in P.p: self.rotate(a,i)
        def rotation_matrix(self,a,e,P):
            if e == -1: x,y,z = P.x, P.y * t.Cos(a) - P.z * t.Sin(a), P.y * t.Sin(a) + P.z * t.Cos(a) 
            if e == 0: x,y,z = P.x * t.Cos(a) + P.z * t.Sin(a),P.y, - P.x * t.Sin(a) + P.z * t.Cos(a) 
            if e == 1: x,y,z = P.x * t.Cos(a) - P.y * t.Sin(a), P.x * t.Sin(a) + P.y * t.Cos(a) ,P.z
            return Coords().Point((x,y,z))
    class Plane: # Plane perpendicular to vector which passes through point A of the vector
        def __init__(self,v):
            self.v = v
        def showFunc(self,img,p):
            P = self.adapt(p)
            P.show(img)
        def adapt(self,p): # Project objects on the plane
            b,c = self.v.calc()
            ux,uy,uz = -self.v.A.x, -self.v.A.y, -self.v.A.z
            P1 = p.copy()
            P1.move((ux,uy,uz))
            P = self.v.rotation_matrix(-c,-1,self.v.rotation_matrix(b-90,0,P1))
            P.move((250,250,0))
            return P
        def show(self,img,P=None):
            if P is None: 
                for i in self.v.A.l: self.show(img,i)
            else:
                if P.t == 0:
                    self.showFunc(img,P)
                    for i in P.l: self.show(img,i)
                if P.t == 1:
                    a = self.adapt(P.A)
                    b = self.adapt(P.B)
                    Coords().Vector((a,b)).show(img)
                    for i in P.A.l: self.show(img,i)
                if P.t == 2:
                    p = []
                    for i in P.p: p.append(self.adapt(i))
                    Coords().Figure(p).show(img)
    class Figure: # Collection of points
        def __init__(self,p): self.p,self.l,self.r,self.t = p,len(p),range(len(p)),2
        def show(self,img):
            for i in self.r: self.p[i].show(img,False)
            for i in range(self.l-1):
                cv.line(img,(int(self.p[i].x),int(self.p[i].y)),(int(self.p[i+1].x),int(self.p[i+1].y)),(200,200,0),4)
            cv.line(img,(int(self.p[0].x),int(self.p[0].y)),(int(self.p[self.l-1].x),int(self.p[self.l-1].y)),(200,200,0),4)         
        def move(self,c):
            for i in self.p: i.move(c)
        def change(self,c):
            for i in self.p: i.change(c)
        def copy(self): return Coords().Figure(self.p)
        def supercopy(self): 
            p = []
            for i in self.r: p.append(i.supercopy())
            return Coords().Figure(p)

if __name__ == "__main__": 
    c = Coords()
    P = c.Point((350,300,0))
    A = c.Point((251,251,1),[P])
    B = c.Point((249,251,1))
    v = c.Vector((A,B))
    p = c.Plane(v)
    while True:
        img = 0 * np.ones((500,500,3),dtype = np.uint8)
        img2 = 0 * np.ones((500,500,3),dtype = np.uint8)
        v.rotate(1)
        print(P.y)
        v.show(img)
        p.show(img2)
        cv.imshow('IMAGE',img)
        cv.imshow('IMAGE2',img2)
        time.sleep(0.01)
        if cv.waitKey(1) & 0xFF == ord(' '): break
    cv.destroyAllWindows() 