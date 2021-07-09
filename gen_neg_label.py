import cv2
import os
# import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
import shutil
import matplotlib.pyplot as plt
import xml.dom.minidom
import random
import shutil
import copy

def get_bbox_xyxy(obj):
    vehicle_class=obj.find("name").text.strip()
    bbox=obj.find("bndbox")
    xmin=int(bbox.find("xmin").text)
    ymin=int(bbox.find("ymin").text)
    xmax=int(bbox.find("xmax").text)
    ymax=int(bbox.find("ymax").text)
    return [vehicle_class,xmin,ymin,xmax,ymax]


def mk_dir(dir_list):    
    for dir in dir_list:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)

def convert_label(vehicle_class):
    if vehicle_class=="car":
        return 1
    elif vehicle_class=="bus":
        return 2
    elif vehicle_class=="truck":
        return 3
    else:
        return 0

def crop_image(image_path):
    _,ext=os.path.splitext(image_path)
    #print(ext)
    xml_path=image_path.replace(ext,".xml")
    print(xml_path)
    _,image_name=os.path.split(image_path)
    if os.path.exists(xml_path):
        tree=ET.parse(xml_path)
        root=tree.getroot()
        image=cv2.imread(image_path)
        if image is not None:
            image_h=image.shape[0]
            image_w=image.shape[1]
            obj_num=0
            for obj in root.iter('object'):
                if obj is not None:
                    bbox=get_bbox_xyxy(obj)
                    xmin=bbox[1]
                    ymin=bbox[2]
                    xmax=bbox[3]
                    ymax=bbox[4]
                    box_w=xmax-xmin
                    box_h=ymax-ymin
        #             ##################jit#################
        #             # if box_w>100 and box_h>100:
        #             #     for jit_num in range(5):
        #             #         new_xmin=int(xmin+box_w*(random.randint(30,50)/100)*random.randint(-1,1))
        #             #         if new_xmin<1:
        #             #             new_xmin=1
        #             #         new_ymin=int(ymin+box_h*(random.randint(30,50)/100)*random.randint(-1,1))
        #             #         if new_ymin<1:
        #             #             new_ymin=1
        #             #         new_xmax=int(xmax+box_w*(random.randint(30,50)/100)*random.randint(-1,1))
        #             #         if new_xmax>image_w:
        #             #             new_xmax=image_w
        #             #         new_ymax=int(ymax+box_h*(random.randint(30,50)/100)*random.randint(-1,1))
        #             #         if new_ymax>image_h:
        #             #             new_ymax=image_h
        #             # elif 50<box_w<100 and 50<box_h<100:
        #             #     for jit_num in range(5):
        #             #         new_xmin=int(xmin+box_w*(random.randint(10,30)/100)*random.randint(-1,1))
        #             #         if new_xmin<1:
        #             #             new_xmin=1
        #             #         new_ymin=int(ymin+box_h*(random.randint(10,30)/100)*random.randint(-1,1))
        #             #         if new_ymin<1:
        #             #             new_ymin=1
        #             #         new_xmax=int(xmax+box_w*(random.randint(10,30)/100)*random.randint(-1,1))
        #             #         if new_xmax>image_w:
        #             #             new_xmax=image_w
        #             #         new_ymax=int(ymax+box_h*(random.randint(10,30)/100)*random.randint(-1,1))
        #             #         if new_ymax>image_h:
        #             #             new_ymax=image_h
        #             # else:
        #             #     jit_num=-1
        #             #     new_xmin=xmin
        #             #     new_ymin=ymin
        #             #     new_xmax=xmax
        #             #     new_ymax=ymax
                    jit_num=-1
                    new_xmin=xmin-int(box_w*0.2)
                    if new_xmin<1:
                        new_xmin=1
                    new_ymin=ymin-int(box_h*0.2)
                    if new_ymin<1:
                        new_ymin=1
                    new_xmax=xmax+int(box_w*0.2)
                    if new_xmax>image_w:
                        new_xmax=image_w
                    new_ymax=ymax+int(box_h*0.2)
                    if new_ymax>image_h:
                        new_ymax=image_h

                    crop_image=image[new_ymin:new_ymax,new_xmin:new_xmax]
                    crop_image=copy.copy(crop_image)
                    
                    

                    xmin=xmin-new_xmin
                    if xmin<1:
                        xmin=1
                    ymin=ymin-new_ymin
                    if ymin<1:
                        ymin=1
                    xmax=xmin+image_w
                    if xmax>image_w:
                        xmax=image_w
                    ymax=ymin+image_h
                    if ymax>image_h:
                        ymax=image_h
                    vehicle_class=bbox[0]
                    # vehicle_class=convert_label(vehicle_class)
                    image_save_path='./images_train/'+image_name.replace(ext,'')+'_object_'+str(obj_num)+'.jpg'
                        #cv2.rectangle(crop_image,(xmin,ymin),(xmin+box_w,ymin+box_h),(0,255,0),2,1)
                        #cv2.putText(crop_image,vehicle_class,(xmin+15,ymin+15),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
                    cv2.imwrite(image_save_path,crop_image)
                    fd_train.write(image_save_path+" "+str(xmin)+" "+str(ymin)+" "+str(xmin+box_w)+" "+str(ymin+box_h)+" "+vehicle_class+"\n")
                    # if file_num<8000:
                    #     image_save_path='./images_train/'+image_name.replace(ext,'')+'_object_'+str(obj_num)+'.jpg'
                    #     #cv2.rectangle(crop_image,(xmin,ymin),(xmin+box_w,ymin+box_h),(0,255,0),2,1)
                    #     #cv2.putText(crop_image,vehicle_class,(xmin+15,ymin+15),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
                    #     cv2.imwrite(image_save_path,crop_image)
                    #     fd_train.write(image_save_path+" "+str(xmin)+" "+str(ymin)+" "+str(xmin+box_w)+" "+str(ymin+box_h)+" "+vehicle_class+"\n")
                    # else:
                    #     image_save_path='./images_val/'+image_name.replace(ext,'')+'_object_'+str(obj_num)+'.jpg'
                    #     #cv2.rectangle(crop_image,(xmin,ymin),(xmin+box_w,ymin+box_h),(0,255,0),2,1)
                    #     #cv2.putText(crop_image,vehicle_class,(xmin+15,ymin+15),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
                    #     cv2.imwrite(image_save_path,crop_image)
                    #     fd_val.write(image_save_path+" "+str(xmin)+" "+str(ymin)+" "+str(xmin+box_w)+" "+str(ymin+box_h)+" "+vehicle_class+"\n")
                    obj_num+=1




            
                # # crop_image=image[ymin:ymax,xmin:xmax]
                # if bbox[0]=='car':
                #     image_save_path='./car/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'_jit_'+str(jit_num)+'.jpg'
                #     #image_save_path='./car/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'.jpg'
                #     cv2.imwrite(image_save_path,crop_image)
                # elif bbox[0]=='bus':
                #     image_save_path='./bus/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'_jit_'+str(jit_num)+'.jpg'
                #     #image_save_path='./bus/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'.jpg'
                #     cv2.imwrite(image_save_path,crop_image)
                # elif bbox[0]=='truck':
                #     image_save_path='./truck/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'_jit_'+str(jit_num)+'.jpg'
                #     #image_save_path='./truck/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'.jpg'
                #     cv2.imwrite(image_save_path,crop_image)
                # obj_num+=1

        
            
            

if __name__=='__main__':
    input_dir='./neg_val'
    # output_dirs=['car','bus','truck']
    # expand_ratio=0.08
    # mk_dir(output_dirs)
    # x=[]
    # y=[]
    # i=0 
    # if os.path.exists("./images_train"):
    #     shutil.rmtree("./images_train")
    # if os.path.exists("./images_val"):
    #     shutil.rmtree("./images_val")
    # os.mkdir("./images_train")
    # os.mkdir("./images_val")
    fd=open(input_dir+'.txt','w')
    # fd_val=open('./neg_val.txt','w')
    file_num=0
    for root,dirs,files in os.walk(input_dir):
        for file in files:
            file_path=os.path.join(root,file)
            img=cv2.imread(file_path)
            h=img.shape[0]
            w=img.shape[1]
            print("img_name:%s"%file,"h=%s"%h,"w=%s"%w)
            if input_dir=='./neg_train':
                fd.write("./images_train/neg_train/"+file+" "+"0"+" "+"0"+" "+str(w)+" "+str(h)+" "+"other"+"\n")
            else:
                fd.write("./images_val/neg_val/"+file+" "+"0"+" "+"0"+" "+str(w)+" "+str(h)+" "+"other"+"\n")

            # f,ext=os.path.splitext(file_path)

            # if ext=='.jpg' or ext=='.png':
            #     image_path=file_path
            #     print(image_path)
            #     crop_image(image_path)
            file_num+=1
            print(file_num)
    fd.close()
    # fd_val.close()
            

            # _,image_name=os.path.split(image_path)
            # f,ext=os.path.splitext(image_path)
            # if ext=='.jpg' or ext=='.png':
            #     xml_path=f+'.xml'
            # image=cv2.imread(image_path)
            # if image is None:
            #     continue
            # image_h=image.shape[0]
            # image_w=image.shape[1]
            # print(image_h,image_w)
            # x.append(image_w)
            # y.append(image_h)
            # print(image_path)
            # gen_small_image_xml(image,xml_path,image_name,image_h,image_w,expand_ratio)
            # crop_image(image_path)
            # i+=1
    # plt.scatter(x,y)
    # plt.xlabel("image width")
    # plt.ylabel("image height")                
    # plt.savefig("distribution.png")
