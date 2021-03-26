import cv2
import os
from math import floor
rootpath='./zhitodata'
labelpath='./zhitodata/labels'
imagepath='./zhitodata/images'
if not os.path.exists('./zhitodata/car'):
    os.mkdir('./zhitodata/car')
if not os.path.exists('./zhitodata/bus'):
    os.mkdir('./zhitodata/bus')
if not os.path.exists('./zhitodata/truck'):
    os.mkdir('./zhitodata/truck')



labelfiles=os.listdir(labelpath)
# imagefiles=os.listdir(imgpath)
# print(labelfiles)
for labelfile in labelfiles:
    imagefile=labelfile.replace('txt','jpg')
    # print(labelfile,imagefile)

    labelfilepath=os.path.join(labelpath,labelfile)
    imagefilepath=os.path.join(imagepath,imagefile)
    print(labelfilepath,imagefilepath)
    with open(labelfilepath) as f:
        try:
            lines=f.readlines()
            i=0
            for line in lines:
                element=line.strip('\n').split(' ')
                x1=round(float(element[1]))
                y1=round(float(element[2]))
                x2=round(float(element[3]))
                y2=round(float(element[4]))
                if (int(element[0])==17 and float(element[5])<0.5):
                    img=cv2.imread(imagefilepath)
                    img_crop=img[y1:y2,x1:x2]
                    if (img_crop.size>0):
                        print(rootpath+'/car/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg')
                        cv2.imwrite(rootpath+'/car/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg',img_crop)
                        print('got one')
                if (int(element[0])==18 and float(element[5])<0.5):
                    img=cv2.imread(imagefilepath)
                    img_crop=img[y1:y2,x1:x2]
                    if (img_crop.size>0):
                        print(rootpath+'/bus/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg')
                        cv2.imwrite(rootpath+'/bus/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg',img_crop)
                        print('got one')
                if (int(element[0])==19 and float(element[5])<0.5):
                    img=cv2.imread(imagefilepath)
                    img_crop=img[y1:y2,x1:x2]
                    if (img_crop.size>0):
                        print(rootpath+'/van/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg')
                        cv2.imwrite(rootpath+'/van/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg',img_crop)
                        print('got one')
                if (int(element[0])==20 and float(element[5])<0.5):
                    img=cv2.imread(imagefilepath)
                    img_crop=img[y1:y2,x1:x2]
                    if (img_crop.size>0):
                        print(rootpath+'/truck/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg')
                        cv2.imwrite(rootpath+'/truck/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg',img_crop)
                        print('got one')
                if (int(element[0])==21 and float(element[5])<0.5):
                    img=cv2.imread(imagefilepath)
                    img_crop=img[y1:y2,x1:x2]
                    if (img_crop.size>0):
                        print(rootpath+'/dumptruck/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg')
                        cv2.imwrite(rootpath+'/dumptruck/'+imagefile.split('.')[0] + '_' + str(i) + '.jpg',img_crop)
                        print('got one')
                i+=1
        except:
            pass
        # obj_num=len(lines)
        # for i in range(obj_num):
        #     save_cut_name = imagefile.split('.')[0] + '_' + str(i) + '.' + imagefile.split('.')[1]
        #     print(save_cut_name)


                # print('got real car')

            # print(element)
            # vehicle_type=int(element[0])
            # if (vehicle_type==17):
            #     print('got car')

    #         vehicle_type=int(vehicle_type)#car_type
    #         print(type(vehicle_type))

#             location=element[1:]
#             img=cv2.imread(imagefilepath)

#             H=img.shape[0]
#             W=img.shape[1]
#             print('W,H:',W,H)
#             print('car_type,location:',car_type,location)
#             #
#             x=float(location[0])*W
#             y=float(location[1])*H
#             w=float(location[2])*W
#             h=float(location[3])*H
#             print('xywh:',x,y,w,h)

#             x1=int(x-w/2)
#             x2=int(x+w/2)
#             y1=int(y-h/2)
#             y2=int(y+h/2)
#             print('x1x2y1y2:',x1, x2, y1, y2)
#             img_cut=img[x1:x2,y1:y2]
#             # cv2.imshow('img_cut',img_cut)
#             # cv2.waitKey(0)
#         for i in range(obj_num):
#             save_cut_name = imagefile.split('.')[0] + '_' + str(i) + '.' + imagefile.split('.')[1]
#             print(save_cut_name)

        # if car_type==0:
        #     cv2.imwrite(os.path.join(rootpath,'car')+'/'+save_cut_name,img_cut)
        # elif car_type==1:
        #      cv2.imwrite(os.path.join(rootpath, 'bus')+'/'+save_cut_name, img_cut)
        # elif car_type==2:
        #      cv2.imwrite(os.path.join(rootpath, 'truck')+'/'+save_cut_name, img_cut)
        # else :
        #      cv2.imwrite(os.path.join(rootpath, 'background')+'/'+save_cut_name, img_cut)




