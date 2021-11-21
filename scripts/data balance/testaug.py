from PIL import Image, ImageDraw
import numpy as np
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import os
os.environ['DISPLAY'] = ':0'




def rand(a=0, b=1):  
    return np.random.rand() * (b - a) + a



def get_random_data(annotation_line, input_shape, random=True, max_boxes=20, jitter=.5, hue=.1, sat=1.5, val=1.5, proc_img=True):

    line = annotation_line.split(",")
    path = os.path.join("/home/xiaoer/chenchen/yolov5/data/images/train", line[0])
    print(path)
    image = Image.open(path)
    image.show()
    iw, ih = image.size  
    h, w = input_shape    
    box = np.array([np.array(list(map(int, box.split(' ')))) for box in line[1:]])  
   
    new_ar = w/h * rand(1-jitter, 1+jitter)/rand(1-jitter, 1+jitter)  
    scale = rand(.25, 2)   
    if new_ar < 1:
        nh = int(scale * h)
        nw = int(nh * new_ar)
    else:
        nw = int(scale * w)
        nh = int(nw / new_ar)
    image = image.resize((nw, nh), Image.BICUBIC)
    # print(nw,nh)
    dx = int(rand(0, w - nw))
    dy = int(rand(0, h - nh))
    new_image = Image.new('RGB', (w, h), (128, 128, 128))   # (128, 128, 128)代表灰色
    new_image.paste(image, (dx, dy))
    image = new_image

    
    flip = rand() < .5 
    if flip: image = image.transpose(Image.FLIP_LEFT_RIGHT)  
    
    hue = rand(-hue, hue)
    sat = rand(1, sat) if rand()<.5 else 1/rand(1, sat)
    val = rand(1, val) if rand()<.5 else 1/rand(1, val)
    x = rgb_to_hsv(np.array(image) / 255.)  
    x[..., 0] += hue
    x[..., 0][x[..., 0] > 1] -= 1
    x[..., 0][x[..., 0] < 0] += 1
    x[..., 1] *= sat
    x[..., 2] *= val
    x[x > 1] = 1
    x[x < 0] = 0
    image_data = hsv_to_rgb(x)  # numpy array, 0 to 1
  
    max_boxes = min(max_boxes, len(box) if len(box) else 0)
    box_data = np.zeros((max_boxes, 5))
    if len(box) > 0:
        np.random.shuffle(box)
        
        box[:, [1, 3]] = box[:, [1, 3]] * nw / iw + dx
        box[:, [2, 4]] = box[:, [2, 4]] * nh / ih + dy
        
        if flip: box[:, [1, 3]] = w - box[:, [3, 1]]

      
        box[:, 1:3][box[:, 1:3] < 0] = 0
        box[:, 3][box[:, 3] > w] = w
        box[:, 4][box[:, 4] > h] = h
        box_w = box[:, 3] - box[:, 1]
        box_h = box[:, 4] - box[:, 2]
        tmp = np.logical_and(box_w > 1, box_h > 1)
        box = box[np.logical_and(box_w > 1, box_h > 1)]  # discard invalid box
        if len(box) > max_boxes: box = box[:max_boxes]
        box_data[:len(box)] = box

    return image_data, box_data


# 原图片绘制展示
def normal_(annotation_line, input_shape):
  
  
    line = annotation_line.split(",")  
 
    path = os.path.join("/home/xiaoer/chenchen/zengqiang/testquwu/images/train", line[0])
    print(path)
    image = Image.open(path)

    box = np.array([np.array(list(map(int, box.split(' ')[1:]))) for box in line[1:]])
    return image, box

with open("/home/xiaoer/chenchen/yolov5/data/need_aug.txt","r") as f:
    lines = f.readlines()
    """ image_data, box_data = normal_("2_146",line[-1], [640, 640])
    img = image_data



    thickness = 3
    for j in range(len(box_data)):
        left, top, right, bottom = box_data[j][0:]
        draw = ImageDraw.Draw(img)
        for i in range(thickness):
            draw.rectangle([left + i, top + i, right - i, bottom - i], outline=(255, 255, 255))
    img.show()
    img.save("image_save_org.jpg") """
    for line in lines:
  
        tmp = line.split(",")
        image_data, box_data = get_random_data(line, [640, 640])
        print(box_data)
        img = Image.fromarray((image_data * 255).astype(np.uint8))
        img.save("/home/xiaoer/chenchen/yolov5/data/images/train/"+tmp[0].split(".")[0]+"_aug.jpg")
        with open("/home/xiaoer/chenchen/yolov5/data/labels/train/"+tmp[0].split(".")[0]+"_aug.txt","w") as f:
            for j in range(len(box_data)):
                thickness = 3
                left, top, right, bottom = box_data[j][1:]
                [img_width, img_height] = img.size
                
                xmin = min(max(0, left), img_width)
                ymin = min(max(0, top), img_height)
                xmax = min(max(0, right), img_width)
                ymax = min(max(0, bottom), img_height)
                if xmax <= xmin or ymax <= ymin:
                    print("Warning: in '{}' xml, there are some bbox w/h <=0")
                    continue
           
                xcenter = xmin + (xmax - xmin) / 2
                ycenter = ymin + (ymax - ymin) / 2
                w = xmax - xmin
                h = ymax - ymin

          
                xcenter = round(xcenter / img_width, 6)
                ycenter = round(ycenter / img_height, 6)
                w = round(w / img_width, 6)
                h = round(h / img_height, 6)
                class_index = int(box_data[j][0])
                info = [str(i) for i in [class_index, xcenter, ycenter, w, h]]
                if j == 0:
                    f.write(" ".join(info))
                else:
                    f.write("\n" + " ".join(info))
        
                draw = ImageDraw.Draw(img)

                for i in range(thickness):
                    draw.rectangle([left + i, top + i, right - i, bottom - i], outline=(255, 255, 255))
        #img.show()
   
        #img.save("image_save_aug.jpg")