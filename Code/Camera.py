from Thread import Thread,Variable,Runner,Run
from System import PATH, os
import cv2 as cv
import numpy as np
import random

inp = cv.VideoCapture(0) # Capture photos

class Camera(Runner):
    def __init__(self):
        super(Camera,self).__init__(None)
    def init(self):
        self.input = inp
        self.image = Variable(np.zeros((480, 640, 3),dtype=np.uint8)) # Variable carrying images
        
        # Color masks
        self.blue_mask = self.Color_Mask((255,0,0),[100,100,20],[125,255,255])
        self.green_mask = self.Color_Mask((0,255,0),[45,100,0],[90,255,255])
        self.red_mask = self.Color_Mask((0,0,255),[5,255,255],[175,100,20],limit=True)
        self.yellow_mask = self.Color_Mask((0,255,255),[20,100,20],[55,255,255])
        self.black_mask = self.Color_Mask((255,255,255),[0,0,0],[179,150,60])

        self.face_classifier = cv.CascadeClassifier(PATH+'cam/haarcascade_frontalface.xml') # Identify faces
        self.face_recognizer = self.Face_Model("KnownPeople",self.detect_face) # Recognize faces

        self.active_recorder = 0
        self.video_n = 0
        
        self.photograph = Thread(self.photo,loop=True,var=self.image) # Start thread taking photos, these are passed to self.image 
        self.photograph.start()

    def photo(self): # Capture photo
        _, image = self.input.read()
        if self.active_recorder == 1: self.video_recorder.write(cv.flip(image,0))
        return cv.flip(image,-1) # The camera is placed upside down
        
    def draw_dot(self,image): cv.circle(image, (240,320), radius=4, color=(0, 0, 255), thickness=-1)

    def read(self): # Returns current image
        self.output = self.image.read()
        return self.output
    
    def stop(self): # opencv condition to stop loop
        if cv.waitKey(30) & 0xFF == ord(' '): return True
        else: return False
    def show(self,image=np.zeros((480, 640, 3),dtype=np.uint8),name="output"): cv.imshow(name,image) # opencv show frame
    def end(self): # close opencv
        self.photograph.pause()
        self.input.release()
        if self.active_recorder == 1: self.video_recorder.release()
        cv.destroyAllWindows()

    def record(self): # Start recording a video
        if self.active_recorder == 0:
            self.video_recorder = cv.VideoWriter(PATH+'cam/Video{}.avi'.format(self.video_n),cv.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
            self.video_n += 1
            self.active_recorder = 1
        else: self.save_record()
    def save_record(self): # End recording
        if self.active_recorder == 1: self.video_recorder.release()
        self.active_recorder = 0
    def save_photo(self): # Take a photograph
        cv.imwrite(PATH+'cam/Photo{}.jpg'.format(self.video_n),self.read())
        self.video_n += 1
    def photo_route(self): # Take a photograph and return it's route
        self.save_photo()
        return self.video_n-1
    
    def detect_face(self,image,draw=False): # Method to detect the largest face (nearest)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        faces = self.face_classifier.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),maxSize=(200,200))
        result,m = (0,0,0,0),(0,0)
        if len(faces) != 0: result = faces[0]
        for (x,y,w,h) in faces:
            if w >= result[2]: result,m = (x,y,w,h), (int(x+w/2) , int(y+h/2))
        if draw:
            x,y,w,h = result
            cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            cv.circle(image,m,2,(0,255,0),-1)
        return result, m
    def coord(self,image,mode,rec=False,draw=True,mask=None,face_recognizer=None,down=0): # Obtain coords of a face / color
        p,n,c = (0,0),"Unknown",0 # Point, name and number of contours
        if mode == 0: 
            p = self.detect_face(image,draw=draw)[1]
            if rec: n = face_recognizer.recognize(image,draw=draw)
        elif mode == 1: 
            (x,y,w,h),p = mask.detect(image,draw=draw,down=down)
            if rec and (x,y,w,h) != (0,0,0,0):
                contour,_ = cv.findContours(cv.bitwise_not(mask.mask(image))[y:y+h,x:x+w], cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                for i in contour:
                    if cv.contourArea(i) > 200: c+=1
        if rec and mode == 0: return p,n
        elif rec and mode == 1: return p,c
        else: return p
    def panoramic(self,photo_list): # Not panoramic, just stacks frames (faster)
        pano = np.hstack(photo_list)
        cv.imwrite(PATH+'cam/Photo{}.jpg'.format(self.video_n),pano)
        self.video_n += 1
        return self.video_n-1

    class Color_Mask: # Detect color
        def __init__(self,color,color1,color2,area=3000,limit=False):
            self.data = [np.array(color1,np.uint8),np.array(color2,np.uint8),np.array([0,color2[1],color2[2]],np.uint8),np.array([175,color1[1],color1[2]],np.uint8)]
            self.color,self.min,self.limit = color,area,limit
        def mask(self,image): # Obtain only the parts of a determined color
            frameHSV = cv.cvtColor(image,cv.COLOR_BGR2HSV)
            if self.limit == False: return cv.inRange(frameHSV,self.data[0],self.data[1])
            else: return cv.add(cv.inRange(frameHSV,self.data[2] ,self.data[0]),cv.inRange(frameHSV,self.data[3],self.data[1]))
        def contour(self,image,area=3000,more=False): # Obtain contours of a color
            contour,_ = cv.findContours(self.mask(image), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            result,ans = None,[]
            if area == 3000: area = self.min
            if len(contour) != 0: 
                if more == False:
                    result = contour[0]
                    for c in contour:
                        if cv.contourArea(c) > cv.contourArea(result): result = c
                    if cv.contourArea(result) < area: return None
                    else: return cv.convexHull(result)
                else: 
                    for i in contour:
                        if cv.contourArea(i) > area: ans.append(cv.convexHull(i))
                    return ans
        def detect(self,image,area=3000,draw=True,contour=None,down=0): # Obtain a rectangle containing the color 
            if contour is None: contour = self.contour(image,area)
            if contour is not None and draw: cv.drawContours(image, [contour], 0, self.color, 3)
            M = cv.moments(contour)
            if (M["m00"]==0): M["m00"]=1
            mx = int(M["m10"]/M["m00"])
            my = int(M['m01']/M['m00'])
            x,y,w,h = cv.boundingRect(contour)
            if down: my = y+h/3
            if draw: cv.circle(image, (mx,int(my)), 7, self.color, -1)
            return (x,y,w,h),(mx,my)
        def detect_all(self,image,area=3000,draw=True):
            r = []
            for i in self.contour(image,area,more=True): r.append(self.detect(image,area,draw,i))
            return r
        
    class Face_Model: # Model to recognize faces
        def __init__(self,group,detect_method):
            from sklearn.neighbors import KNeighborsClassifier # This library takes time to start
            self.knc = KNeighborsClassifier
            self.dataPath = PATH+'cam/' + group
            self.imagePaths = []
            try: self.imagePaths = os.listdir(self.dataPath)
            except: os.makedirs(self.dataPath)
            self.detect_method = detect_method
            self.feature_net = cv.dnn.readNetFromONNX(PATH+"cam/mobilenetv2.onnx")
            self.knn = None
            self.names = {}
            self.people = []
            self.neighbours = 0
            self.train_knn()
        def features(self,img): # Extract features of an image
            if len(img.shape) == 2: img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
            h, w = img.shape[:2]
            max_dim = max(h, w)
            if len(img.shape) == 2: canvas = np.zeros((max_dim, max_dim), dtype=img.dtype)
            else: canvas = np.zeros((max_dim, max_dim, 3), dtype=img.dtype)
            x_offset = (max_dim - w) // 2
            y_offset = (max_dim - h) // 2
            canvas[y_offset:y_offset+h, x_offset:x_offset+w] = img
            self.feature_net.setInput(cv.dnn.blobFromImage(cv.cvtColor(cv.resize(canvas, (224, 224), interpolation=cv.INTER_AREA), cv.COLOR_BGR2RGB), scalefactor=1.0/127.5, size=(224, 224),mean=(127.5, 127.5, 127.5), swapRB=False, crop=False))
            return self.feature_net.forward().flatten()
        def train_knn(self): # Train model with photos
            embs,n = [],[]
            if not os.path.exists(self.dataPath): os.makedirs(self.dataPath)
            people = os.listdir(self.dataPath)
            self.people = people
            for label_id, person in enumerate(people):
                person_dir = os.path.join(self.dataPath, person)
                self.names[label_id] = person
                for image_file in os.listdir(person_dir):
                    if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        img = cv.imread(os.path.join(person_dir, image_file), cv.IMREAD_UNCHANGED)
                        if img is None: continue
                        feat = self.features(img)
                        embs.append(feat)
                        n.append(label_id)
            self.neighbours = len(people)
            if self.neighbours > 3: self.neighbours = 3
            embs, n = np.array(embs), np.array(n)
            if embs.size > 0: Run(lambda: self.update_knn(embs,n))
        def update_knn(self,embs,n):
                self.knn = self.knc(n_neighbors=self.neighbours)
                self.knn.fit(embs, n)
        def recognition(self,frame,draw=0,reg=1): # Identify name of person
            roi,(x,y,w,h) = self.get_roi(frame)
            if roi is None: return "Nobody talking",0
            feat = self.features(roi).reshape(1, -1)
            if self.knn is None: return "Unknown", roi
            else:
                distances, _ = self.knn.kneighbors(feat, n_neighbors=self.neighbours)
                dist = np.mean(distances)
                if dist > 50.0:
                    name = "Unknown"
                    if draw:
                        cv.putText(frame, "Unknown", (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                        cv.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
                else:
                    name = self.names.get(self.knn.predict(feat)[0], "Unknown")
                    if draw:
                        cv.putText(frame, name, (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                        cv.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                    if reg: self.register(name,roi)
                return name,roi    
        def register(self,name,roi,new=0): 
            person_dir = os.path.join(self.dataPath, name)
            os.makedirs(person_dir, exist_ok=True)
            i = len(os.listdir(person_dir))
            if i > 10: i = random.randint(0,15)
            cv.imwrite(os.path.join(person_dir, name+str(i)+".jpg"), roi)
            if new: self.train_knn()
        def get_roi(self,frame):
            (x,y,w,h),_ = self.detect_method(frame)
            if (x,y,w,h) == (0,0,0,0): return None,(0,0,0,0)
            return  frame[y:y+h, x:x+w],(x,y,w,h)
        def new(self,name,func): # Add a new person
            for i in range(4):
                n,roi = "Nobody",None
                while "Nobody" in n:  # Wait for a person to appear
                    frame = func()
                    n,roi = self.recognition(frame)
                self.register(name,roi)
                t.sleep(0.2)
            self.train_knn()



if __name__ == "__main__":
    cam = Camera()
    while not cam.started: pass
    print("Click [SPACE] to exit.")
    t = ("1" in input())
    while True:
        frame = cam.read()
        if t:
            roi,_ = cam.face_recognizer.get_roi(frame)
            if roi is not None:
                inp = input("Hello! I don`t know you yet, who are you?\n   >>>  I am ")
                if inp: cam.face_recognizer.register(inp,roi,1)
        else:
            name,roi = cam.face_recognizer.recognition(frame,draw=True,reg=0)
        cv.imshow("FRAME", frame)
        if cam.stop(): break
    cam.end()