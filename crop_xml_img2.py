import cv2
import os
import xml.etree.ElementTree as ET
import shutil
import matplotlib.pyplot as plt
import xml.dom.minidom
import random
def get_expand_bbox_xyxy(obj,image_h,image_w,expand_ratio):
    vehicle_class=obj.find("name").text.strip()
    bbox=obj.find("bndbox")
    xmin=int(bbox.find("xmin").text)
    ymin=int(bbox.find("ymin").text)
    xmax=int(bbox.find("xmax").text)
    ymax=int(bbox.find("ymax").text)
    bbox_w=xmax-xmin
    bbox_h=ymax-ymin
    expand_w=int(bbox_w*expand_ratio)
    expand_h=int(bbox_h*expand_ratio)
    xmin_expand=xmin-expand_w
    if xmin_expand<1:
        xmin_expand=1
    xmax_expand=xmax+expand_w
    if xmax_expand>image_w:
        xmax_expand=image_w
    ymin_expand=ymin-expand_h
    if ymin_expand<1:
        ymin_expand=1
    ymax_expand=ymax+expand_h
    if ymax_expand>image_h:
        ymax_expand=image_h
    return [vehicle_class,xmin_expand,ymin_expand,xmax_expand,ymax_expand]  
    

def get_bbox_xyxy(obj):
    vehicle_class=obj.find("name").text.strip()
    bbox=obj.find("bndbox")
    xmin=int(bbox.find("xmin").text)
    ymin=int(bbox.find("ymin").text)
    xmax=int(bbox.find("xmax").text)
    ymax=int(bbox.find("ymax").text)
    return [vehicle_class,xmin,ymin,xmax,ymax]

def gen_xml_flie(new_coordinate,image_save_path,w,h):
    f,ext=os.path.splitext(image_save_path)
    folder_path,image_name=os.path.split(image_save_path)
    xml_path=f+'.xml'
    print(xml_path)

    doc=xml.dom.minidom.Document()
    root=doc.createElement("annotation")
    doc.appendChild(root)

    nodefolderpath=doc.createElement("folder")
    nodefolderpath.appendChild(doc.createTextNode(folder_path))
    nodeimagename=doc.createElement("filename")
    nodeimagename.appendChild(doc.createTextNode(image_name))
    nodeimagepath=doc.createElement("path")
    nodeimagepath.appendChild(doc.createTextNode(image_save_path))
    nodesource=doc.createElement("source")
    nodesource.appendChild(doc.createTextNode("unknown"))
    
    nodesize=doc.createElement("size")
    nodewidth=doc.createElement("width")
    nodewidth.appendChild(doc.createTextNode(str(w)))
    nodeheight=doc.createElement("height")
    nodeheight.appendChild(doc.createTextNode(str(h)))
    nodedepth=doc.createElement("depth")
    nodedepth.appendChild(doc.createTextNode("3"))
    
    nodesegment=doc.createElement("segment")
    nodesegment.appendChild(doc.createTextNode("0"))

    nodesize.appendChild(nodewidth)
    nodesize.appendChild(nodeheight)
    nodesize.appendChild(nodedepth)

    root.appendChild(nodefolderpath)
    root.appendChild(nodeimagename)
    root.appendChild(nodeimagepath)
    root.appendChild(nodesource)
    root.appendChild(nodesize)
    root.appendChild(nodesegment)

    tag=new_coordinate[0]
    xmin=new_coordinate[1]
    ymin=new_coordinate[2]
    xmax=new_coordinate[3]
    ymax=new_coordinate[4]

    nodeobject=doc.createElement("object")
    nodename=doc.createElement("name")
    nodename.appendChild(doc.createTextNode(tag))
    nodetruncated=doc.createElement("truncated")
    nodetruncated.appendChild(doc.createTextNode('0'))
    nodedifficult=doc.createElement("difficult")
    nodedifficult.appendChild(doc.createTextNode('0'))

    nodebndbox=doc.createElement("bndbox")
    nodexmin=doc.createElement("xmin")
    nodexmin.appendChild(doc.createTextNode(str(xmin)))
    nodeymin=doc.createElement("ymin")
    nodeymin.appendChild(doc.createTextNode(str(ymin)))
    nodexmax=doc.createElement("xmax")
    nodexmax.appendChild(doc.createTextNode(str(xmax)))
    nodeymax=doc.createElement("ymax")
    nodeymax.appendChild(doc.createTextNode(str(ymax)))

    nodeobject.appendChild(nodename)
    nodeobject.appendChild(nodetruncated)
    nodeobject.appendChild(nodedifficult)
    nodeobject.appendChild(nodebndbox)
    nodebndbox.appendChild(nodexmin)
    nodebndbox.appendChild(nodeymin)
    nodebndbox.appendChild(nodexmax)
    nodebndbox.appendChild(nodeymax)

    root.appendChild(nodeobject)

    fp = open(xml_path, 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
    fp.close()



def gen_xml_for_expand_vehicle(bbox,expand_bbox,image_save_path):
   
    vehicle_class,xmin,ymin,xmax,ymax=bbox
    w=xmax-xmin
    h=ymax-ymin

    vehicle_class,expand_xmin,expand_ymin,expand_xmax,expand_ymax=expand_bbox
    expand_w=expand_xmax-expand_xmin
    expand_h=expand_ymax-expand_ymin

    new_xmin=xmin-expand_xmin
    if new_xmin<1:
        new_xmin=1
    new_ymin=ymin-expand_ymin
    if new_ymin<1:
        new_ymin=1
    new_xmax=new_xmin+w
    if new_xmax>expand_w:
        new_xmax=expand_w
    new_ymax=new_ymin+h
    if new_ymax>expand_h:
        new_ymax=expand_h
    new_coordinate=[vehicle_class,new_xmin,new_ymin,new_xmax,new_ymax]
    if expand_w>24 and expand_h>24:
        gen_xml_flie(new_coordinate,image_save_path,w,h)


def gen_small_image_xml(image,xml_path,image_name,image_h,image_w,expand_ratio):
    tree=ET.parse(xml_path)
    root=tree.getroot()
    car_num=0
    bus_num=0
    truck_num=0  
 
    for obj in root.iter('object'):
        bbox=get_bbox_xyxy(obj)
        expand_bbox=get_expand_bbox_xyxy(obj,image_h,image_w,expand_ratio)               
        if obj.find('name').text.strip()=='car':
            expand_car_image=image[expand_bbox[2]:expand_bbox[4],expand_bbox[1]:expand_bbox[3],:]
            image_save_path='./'+output_dirs[1]+'/'+str(i)+'_'+output_dirs[1]+'_'+str(car_num)+'.jpg'
            print(image_save_path)
            cv2.imwrite(image_save_path,expand_car_image)
            gen_xml_for_expand_vehicle(bbox,expand_bbox,image_save_path)
            car_num+=1
        elif obj.find('name').text.strip()=='bus':
            expand_bus_image=image[expand_bbox[2]:expand_bbox[4],expand_bbox[1]:expand_bbox[3],:]
            image_save_path='./'+output_dirs[2]+'/'+str(i)+'_'+output_dirs[2]+'_'+str(bus_num)+'.jpg'
            print(image_save_path)
            cv2.imwrite(image_save_path,expand_bus_image)
            gen_xml_for_expand_vehicle(bbox,expand_bbox,image_save_path)
            bus_num+=1
        elif obj.find('name').text.strip()=='truck':
            expand_truck_image=image[expand_bbox[2]:expand_bbox[4],expand_bbox[1]:expand_bbox[3],:]
            image_save_path='./'+output_dirs[3]+'/'+str(i)+'_'+output_dirs[3]+'_'+str(truck_num)+'.jpg'
            print(image_save_path)
            cv2.imwrite(image_save_path,expand_truck_image)
            gen_xml_for_expand_vehicle(bbox,expand_bbox,image_save_path)
            truck_num+=1
        else:
            continue


def mk_dir(dir_list):    
    for dir in dir_list:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.mkdir(dir)

def crop_image(image_path):
    xml_path=image_path.replace(".png",".xml")
    root,image_name=os.path.split(image_path)
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
                if box_w>100 and box_h>100:
                    for jit_num in range(5):
                        new_xmin=int(xmin+box_w*(random.randint(30,50)/100)*random.randint(-1,1))
                        if new_xmin<1:
                            new_xmin=1
                        new_ymin=int(ymin+box_h*(random.randint(30,50)/100)*random.randint(-1,1))
                        if new_ymin<1:
                            new_ymin=1
                        new_xmax=int(xmax+box_w*(random.randint(30,50)/100)*random.randint(-1,1))
                        if new_xmax>image_w:
                            new_xmax=image_w
                        new_ymax=int(ymax+box_h*(random.randint(30,50)/100)*random.randint(-1,1))
                        if new_ymax>image_h:
                            new_ymax=image_h
                elif 50<box_w<100 and 50<box_h<100:
                    for jit_num in range(5):
                        new_xmin=int(xmin+box_w*(random.randint(10,30)/100)*random.randint(-1,1))
                        if new_xmin<1:
                            new_xmin=1
                        new_ymin=int(ymin+box_h*(random.randint(10,30)/100)*random.randint(-1,1))
                        if new_ymin<1:
                            new_ymin=1
                        new_xmax=int(xmax+box_w*(random.randint(10,30)/100)*random.randint(-1,1))
                        if new_xmax>image_w:
                            new_xmax=image_w
                        new_ymax=int(ymax+box_h*(random.randint(10,30)/100)*random.randint(-1,1))
                        if new_ymax>image_h:
                            new_ymax=image_h
                else:
                    jit_num=-1
                    new_xmin=xmin
                    new_ymin=ymin
                    new_xmax=xmax
                    new_ymax=ymax
                crop_image=image[new_ymin:new_ymax,new_xmin:new_xmax]
                # crop_image=image[ymin:ymax,xmin:xmax]
                if bbox[0]=='car':
                    image_save_path='./car/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'_jit_'+str(jit_num)+'.jpg'
                    #image_save_path='./car/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'.jpg'
                    cv2.imwrite(image_save_path,crop_image)
                elif bbox[0]=='bus':
                    image_save_path='./bus/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'_jit_'+str(jit_num)+'.jpg'
                    #image_save_path='./bus/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'.jpg'
                    cv2.imwrite(image_save_path,crop_image)
                elif bbox[0]=='truck':
                    image_save_path='./truck/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'_jit_'+str(jit_num)+'.jpg'
                    #image_save_path='./truck/'+image_name.replace('.png','')+'_object_'+str(obj_num)+'.jpg'
                    cv2.imwrite(image_save_path,crop_image)
                obj_num+=1

        
            
            

if __name__=='__main__':
    input_dir='./data'
    output_dirs=['car','bus','truck']
    # expand_ratio=0.08
    mk_dir(output_dirs)
    # x=[]
    # y=[]
    # i=0 
    for root,dirs,files in os.walk(input_dir):
        for file in files:
            image_path=os.path.join(root,file)
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
            print(image_path)
            # gen_small_image_xml(image,xml_path,image_name,image_h,image_w,expand_ratio)
            crop_image(image_path)
            # i+=1
    # plt.scatter(x,y)
    # plt.xlabel("image width")
    # plt.ylabel("image height")                
    # plt.savefig("distribution.png")
