import os
import shutil
import random

train_latbel_path = "/home/xiaoer/chenchen/yolov5/data/labels/train"
test_latbel_path = "/home/xiaoer/chenchen/yolov5/data/labels/test"
val_latbel_path = "/home/xiaoer/chenchen/yolov5/data/labels/val"
if  os.path.exists(train_latbel_path):
    shutil.rmtree(train_latbel_path)
os.makedirs(train_latbel_path)
if  os.path.exists(test_latbel_path):
    shutil.rmtree(test_latbel_path)
os.makedirs(test_latbel_path)
if  os.path.exists(val_latbel_path):
    shutil.rmtree(val_latbel_path)
os.makedirs(val_latbel_path)

train_images_path = "/home/xiaoer/chenchen/yolov5/data/images/train"
test_images_path = "/home/xiaoer/chenchen/yolov5/data/images/test"
val_images_path = "/home/xiaoer/chenchen/yolov5/data/images/val"
if  os.path.exists(train_images_path):
    shutil.rmtree(train_images_path)
os.makedirs(train_images_path)
if  os.path.exists(test_images_path):
    shutil.rmtree(test_images_path)
os.makedirs(test_images_path)
if  os.path.exists(val_images_path):
    shutil.rmtree(val_images_path)
os.makedirs(val_images_path)

#split dataset accroding 8:1:1
nums = random.sample(range(1,9733),2000)
nums = list(set(nums))
test = nums[:len(nums)//2]
print(len(test))
val = nums[len(nums)//2:]
print(len(val))
count0 = 0
count1 = 0
count2 = 0
count3 = 0
for root, dirs, files in os.walk("/home/xiaoer/chenchen/yolov5/data/labels_org"):
    count0+=1
    for index,file in enumerate(files):
        if index in test:
            if not os.path.exists(os.path.join(test_latbel_path,file)):
                shutil.copy(os.path.join(root,file),test_latbel_path)
            shutil.copy(os.path.join("/home/xiaoer/chenchen/yolov5/data/images_org",file.split(".")[0]+".jpg"),test_images_path)
            count1+=1
        elif index in val:
            if not os.path.exists(os.path.join(val_latbel_path,file)):
                shutil.copy(os.path.join(root,file),val_latbel_path)
            shutil.copy(os.path.join("/home/xiaoer/chenchen/yolov5/data/images_org",file.split(".")[0]+".jpg"),val_images_path)
            count2+=1
        else:
            if not os.path.exists(os.path.join(train_latbel_path,file)):
                shutil.copy(os.path.join(root,file),train_latbel_path)
            shutil.copy(os.path.join("/home/xiaoer/chenchen/yolov5/data/images_org",file.split(".")[0]+".jpg"),train_images_path)
            count3+=1
           
print(count0)
print(count1) 
print(count2)
print(count3)