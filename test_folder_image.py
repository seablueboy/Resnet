import cv2
import os
import torch
from torchvision import transforms
import shutil


image_transforms = {
    'train': transforms.Compose([
        #transforms.RandomResizedCrop(224),
        #RandAugment(3,4),
        transforms.Resize((128,128)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.15, 0.15, 0.15),
        transforms.RandomRotation(degrees=15),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ]),
    'test': transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((160,160)),
        transforms.Normalize(mean = [0.5, 0.5, 0.5], std = [0.5, 0.5, 0.5])
    ])
}

def get_boxes(label_path):
    boxes=[]
    file=open(label_path)
    lines=file.readlines()
    for line in lines:
        line=line.strip().split()
        type=line[0]
        xmin=line[1]
        ymin=line[2]
        xmax=line[3]
        ymax=line[4]
        box=[type,xmin,ymin,xmax,ymax]
        boxes.append(box)
    return boxes
    
def letterbox(image,expected_size):
    ih, iw = image.shape[0:2]
    ew, eh = expected_size
    scale = min(eh / ih, ew / iw)
    nh = int(ih * scale)
    nw = int(iw * scale)
    image = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_CUBIC)
    top = (eh - nh) // 2
    bottom = eh - nh - top
    left = (ew - nw) // 2
    right = ew - nw - left
    new_img = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT,value=(128,128,128))
    return new_img

def make_dir(dir):    
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)

def convert_label(label):
    if label=="0":
        label="unknown"
    elif label=="1":
        label="car"
    elif label=="2":
        label="bus"
    elif label=="3":
        label="truck"
    else:
        pass
    return label

    

device=torch.device("cuda:3")
inputdir='./trt_test/images'
outputdir='./draw_images/'
make_dir(outputdir)
model=torch.load("best_model_20210423.pth")
model.to(device)
model.eval()

for root,dirs,files in os.walk(inputdir):
    i=0
    for file in files:
        image_path=os.path.join(root,file)
        img=cv2.imread(image_path)
        _,ext=os.path.splitext(image_path)
        label_path=image_path.replace("images","labels").replace(ext,".txt")
        print(label_path)
        boxes=get_boxes(label_path)
        for box in boxes:
            small_image=img[int(box[2]):int(box[4]),int(box[1]):int(box[3])]
            small_image=cv2.cvtColor(small_image,cv2.COLOR_BGR2RGB)
            small_image=letterbox(small_image,(160,160))
            transform=image_transforms['test']
            small_image=transform(small_image)
            small_image=small_image.to(device)
            small_image=small_image.view(1,3,160,160)
            label=model(small_image)
            _,label=label.topk(1,1,True,True)
            # print(label[0].cpu().numpy()[0])
            label=label[0].cpu().numpy()[0]
            label=str(label)
            label=convert_label(label)
            print(label)
            cv2.rectangle(img,(int(box[1]),int(box[2])),(int(box[3]),int(box[4])),(0,255,0))
            cv2.putText(img,label,(int(box[1])+5,int(box[2])+5),cv2.FONT_HERSHEY_PLAIN,2,(0, 0, 255))
        cv2.imwrite(outputdir+str(i)+'.jpg',img)
        i+=1








                
         




