import os
import cv2
def cv2_letterbox_image(image, expected_size):
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
    new_img = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT,value=(114,114,114))
    return new_img

import os
dir="./zhito_carclass_datasets"
# f=open("dir.txt","w")
for root,dirs,files in os.walk(dir):
    for file in files:
        file_path=os.path.join(root,file)
        image=cv2.imread(file_path)
        new_img=cv2_letterbox_image(image,(160,160))
        cv2.imwrite(file_path,new_img)
        # print(new_img.shape)
        # print(os.path.join(root,file)+"\n")
        # f.writelines(os.path.join(root,file)+"\n") 