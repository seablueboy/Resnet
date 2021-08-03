# import json
# import os
# import cv2
# import xml.dom.minidom


# def gen_xml_flie(object_list,image_path,w,h):
#     xml_path=image_path.replace('.png','.xml')
#     # f,ext=os.path.splitext(image_path)
#     folder_path,image_name=os.path.split(image_path)
    
#     print(xml_path)

#     doc=xml.dom.minidom.Document()
#     root=doc.createElement("annotation")
#     doc.appendChild(root)

#     nodefolderpath=doc.createElement("folder")
#     nodefolderpath.appendChild(doc.createTextNode(folder_path))
#     nodeimagename=doc.createElement("filename")
#     nodeimagename.appendChild(doc.createTextNode(image_name))
#     nodeimagepath=doc.createElement("path")
#     nodeimagepath.appendChild(doc.createTextNode(image_path))
#     nodesource=doc.createElement("source")
#     nodesource.appendChild(doc.createTextNode("unknown"))
    
#     nodesize=doc.createElement("size")
#     nodewidth=doc.createElement("width")
#     nodewidth.appendChild(doc.createTextNode(str(w)))
#     nodeheight=doc.createElement("height")
#     nodeheight.appendChild(doc.createTextNode(str(h)))
#     nodedepth=doc.createElement("depth")
#     nodedepth.appendChild(doc.createTextNode("3"))
    
#     nodesegment=doc.createElement("segment")
#     nodesegment.appendChild(doc.createTextNode("0"))

#     nodesize.appendChild(nodewidth)
#     nodesize.appendChild(nodeheight)
#     nodesize.appendChild(nodedepth)

#     root.appendChild(nodefolderpath)
#     root.appendChild(nodeimagename)
#     root.appendChild(nodeimagepath)
#     root.appendChild(nodesource)
#     root.appendChild(nodesize)
#     root.appendChild(nodesegment)

#     for obj in object_list:
#         tag=obj[0]
#         xmin=obj[1]
#         ymin=obj[2]
#         xmax=obj[3]
#         ymax=obj[4]

#         nodeobject=doc.createElement("object")
#         nodename=doc.createElement("name")
#         nodename.appendChild(doc.createTextNode(tag))
#         nodetruncated=doc.createElement("truncated")
#         nodetruncated.appendChild(doc.createTextNode('0'))
#         nodedifficult=doc.createElement("difficult")
#         nodedifficult.appendChild(doc.createTextNode('0'))

#         nodebndbox=doc.createElement("bndbox")
#         nodexmin=doc.createElement("xmin")
#         nodexmin.appendChild(doc.createTextNode(str(xmin)))
#         nodeymin=doc.createElement("ymin") 
#         nodeymin.appendChild(doc.createTextNode(str(ymin)))
#         nodexmax=doc.createElement("xmax")
#         nodexmax.appendChild(doc.createTextNode(str(xmax)))
#         nodeymax=doc.createElement("ymax")
#         nodeymax.appendChild(doc.createTextNode(str(ymax)))

#         nodeobject.appendChild(nodename)
#         nodeobject.appendChild(nodetruncated)
#         nodeobject.appendChild(nodedifficult)
#         nodeobject.appendChild(nodebndbox)
#         nodebndbox.appendChild(nodexmin)
#         nodebndbox.appendChild(nodeymin)
#         nodebndbox.appendChild(nodexmax)
#         nodebndbox.appendChild(nodeymax)

#         root.appendChild(nodeobject)

#     fp = open(xml_path, 'w')
#     doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")
#     print("got one")
#     fp.close()




# all_images_path='D:/cleaned_data/J7A02/threshold06'
# f = open('03_09.json',"r",encoding="utf-8")
# json_data = json.load(f)
# f.close()
# if os.path.exists("./save"):
#     shutil.rmtree('./save')
# os.mkdir('./save')
# #print(type(json_list))
# # k=json_data.keys()
# # print(json_data["annotations"])
# # #print(json_list)
# # print(len(json_data["annotations"])) #200 examples

# # print(json_data["annotations"][0])

# #print(json_data["annotations"][0]['labels_box2D'][0]) #labels_box2D is a list start with "attributes"
# # print(json_data["annotations"][0]['fileuri'])#file_name
# # for i in range (len(json_data["annotations"][0]['labels_box2D'])):
# #     print(json_data["annotations"][0]['labels_box2D'][i])








# #step1 save all 200 image_names and json_content:
# image_list=[]
# json_list=[]
# for i in range(len(json_data["annotations"])):
#     # print(json_data["annotations"][i]['fileuri'].split('/')[-1]) #200 file names
#     image_name=json_data["annotations"][i]['fileuri'].split('/')[-1]
#     json_content=json_data["annotations"][i]
#     #jsonfile_name=image_name.replace('.png','.json')
#     # with open('./'+jsonfile_name,'w') as f:
#     #     f.write(str(json_data["annotations"][i]))
    
#     # print(json_name)
#     image_list.append(image_name)
#     json_list.append(json_content)




# #step2  match images in datasets and match coresponding jsons in two times
# for root, dirs, files in os.walk(all_images_path):
#     for file in files:

#         if file in image_list:
#             #save image
#             image_path=os.path.join(root,file)
#             img=cv2.imread(image_path)
#             cv2.imwrite("./save/"+file,img)

#             for json_element in json_list:
#                 if json_element['fileuri'].split('/')[-1]==file:
#                    jsonfile_name=file.replace(".png",'.json')
#                    with open('./save/'+jsonfile_name,'w') as f:
#                        json.dump(json_element,f)

# #step 3 convert jason files to xml files
# for json_element in json_list:
#     json_path="./save/"+json_element['fileuri'].split('/')[-1].replace('.png','.json')
#     image_path="./save/"+json_element['fileuri'].split('/')[-1]
#     xml_path='./save/'+image_name.replace('.png','.xml')
#     print(json_path,image_path)
#     # print(json_path)
#     with open(json_path) as f:
#         data=json.load(f)
#         # if 'labels_box2D' not in data:
#         # print(json_path)
#         # print("################")
#         # print(json_element)
#         if 'labels_box2D' not in json_element:
#             f.close()
#             os.remove(json_path)
#             os.remove(image_path)
#             continue

#         img=cv2.imread(image_path)
#         h=img.shape[0]
#         w=img.shape[1]
#         object_list=[]
#         for i in range(len(data['labels_box2D'])):
#                 # print(data['labels_box2D'][i]['category'],data['labels_box2D'][i]['box2D'][0]['x'],data['labels_box2D'][i]['box2D'][0]['y'],data['labels_box2D'][i]['box2D'][1]['x'],data['labels_box2D'][i]['box2D'][1]['y'])
#                 if data['labels_box2D'][i]['category']=='car' or data['labels_box2D'][i]['category']=='bus' or data['labels_box2D'][i]['category']=='truck':
#                     obj=[data['labels_box2D'][i]['category'],data['labels_box2D'][i]['box2D'][0]['x'],data['labels_box2D'][i]['box2D'][0]['y'],data['labels_box2D'][i]['box2D'][1]['x'],data['labels_box2D'][i]['box2D'][1]['y']]
#                     # print(data['labels_box2D'][i]['category'],data['labels_box2D'][i]['box2D'][0]['x'],data['labels_box2D'][i]['box2D'][0]['y'],data['labels_box2D'][i]['box2D'][1]['x'],data['labels_box2D'][i]['box2D'][1]['y'])
#                     object_list.append(obj)
#         print(object_list)
#         gen_xml_flie(object_list,image_path,w,h)

import os
import fileinput
fd=open('./labels_train.txt')
# label_file='./labels_train.txt'
fd_new=open('./labels_train_new.txt','w')
images_path='./images_train/mask'
# labels=[]
# for line in fd:
#     #image_name=line.split(' ')[0].replace('./images_train/','')
#     labels.append(line)
    # print (line)
# print('#####################################')
# print (labels)
file_num=0
file_names=[]
for root, dirs, files in os.walk(images_path):
    for file in files:
        file_names.append(file)
for line in fd:
    if line.split(" ")[0].split("/")[-1] in file_names:
        print(line.strip().split(" ")[-1])
        # print(type(line))
        # line.replace(line.strip().split(" ")[-1],"mask")
        # print(type(line.strip().split(" ")))
        linelist=line.strip().split(" ")
        print(type(linelist[0]))
        # print(linelist[0].replace(linelist[0].split("/")[2],'mask'))
        linelist[0]=linelist[0].replace(linelist[0].split("/")[2],'mask')
        # print(linelist[0].split("/")[2])
        linelist[-1] = 'mask'
        line=" ".join(linelist)+"\n"
        # line=str(linelist)
        # print(line)
        # line.strip().split(" ")[-1]='mask'
        print(linelist)
        # print(line_join)
        print(line)
    fd_new.write(line)

fd_new.close()
fd.close()

        # print(line.split(" ")[0].split("/")[-1])

        # print(line.split(" ")[-1])

    # print(line.split(" ")[0].split("/")[-1])



        # print(file)
        # for label in labels:
        #     # if file == label.split(' ')[0].replace('./images_train/',''):
        #     if file==label.split(" ")[0].split("/")[-1]:

        #         fd_new.write(label)
        #         print(file)
        #         file_num+=1
        #         print((file_num))

#             #save image
#             image_path=os.path.join(root,file)
#             img=cv2.imread(image_path)
#             cv2.imwrite("./save/"+file,img)

