import cv2
import os 
import shutil
from PIL import Image, ImageStat
import math

def brightness(path):
    im = Image.open(path)
    stat = ImageStat.Stat(im)
    r,g,b = stat.mean
    return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068 *(b**2))
def getImageVar(imgPath):
    image = cv2.imread(imgPath)
    if image is not None:
        img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_var = cv2.Laplacian(img2gray, cv2.CV_64F).var()
        if image_var is not None:
            return image_var
        else:
            return -1

dir_del=["./car_del","./bus_del","./truck_del"]
for dir in dir_del:
    if not os.path.exists(dir):
       os.mkdir(dir)
       print(dir)
    
    

###########car###############
image_dir="./car"
i=0
j=0
for root, dirs, files in os.walk(image_dir):
    for file in files:
        image_path=os.path.join(root,file)
        image=cv2.imread(image_path)
        h=image.shape[0]
        w=image.shape[1]
        image_var=getImageVar(image_path)
        bright=brightness(image_path)
        #print(image_path)
        if image_var is None:
            os.remove(image_path)
        elif ((image_var<800 and w<50 and h<50) or  w<40 or h<40 or (int(h/w)>5) or (int(w/h)>5) or (bright<80 and w<50 and h<50)or bright<60): ###car
            print(image_path)
            print(image_var)
            shutil.move(image_path,'./car_del/'+file)
            i+=1
        j+=1
print("total:%d"%j,"moved:%d"%i)

##########bus#################
image_dir="./bus"
i=0
j=0
for root, dirs, files in os.walk(image_dir):
    for file in files:
        image_path=os.path.join(root,file)
        image=cv2.imread(image_path)
        h=image.shape[0]
        w=image.shape[1]
        image_var=getImageVar(image_path)
        bright=brightness(image_path)
        #print(image_path)
        if image_var is None:
            os.remove(image_path)
        elif ((image_var<800 and w<50 and h<50) or  w<40 or h<40 or (int(h/w)>5) or (int(w/h)>5)  or (bright<80 and w<50 and h<50) or bright<60): ###bus
            print(image_path)
            print(image_var)
            shutil.move(image_path,'./bus_del/'+file)
            i+=1
        j+=1
print("total:%d"%j,"moved:%d"%i)

############truck################
image_dir="./truck"
i=0
j=0
for root, dirs, files in os.walk(image_dir):
    for file in files:
        image_path=os.path.join(root,file)
        image=cv2.imread(image_path)
        h=image.shape[0]
        w=image.shape[1]
        image_var=getImageVar(image_path)
        bright=brightness(image_path)
        #print(image_path)
        if image_var is None:
            os.remove(image_path)
        elif ((image_var<800 and w<50 and h<50) or  w<40 or h<40 or (int(h/w)>5) or (int(w/h)>5)  or (bright<80 and w<50 and h<50)or bright<60): ###truck
            print(image_path)
            print(image_var)
            shutil.move(image_path,'./truck_del/'+file)
            i+=1
        j+=1
print("total:%d"%j,"moved:%d"%i)