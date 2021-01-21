"""
创建类似coco数据集annotations文件夹下的instances_train2017.json文件。
annotations字段：
    category_id：该注释的类别id
    id：当前注释的id
    image_id：该注释所在的图片的id号
    area：区域面积
    bbox:目标的矩形标注框
    iscrowd:0或1。0表示标注的单个对象，此时segmentation使用polygon表示，
    1表示标注的是一组对象，此时segmentation使用RLE格式
    segmentation：若使用polygon标注时，则记录的是多边形的坐标点，连续两个数值表示一个点的坐标位置，因此此时点的数量为偶数
                    若使用RLE格式（Run Length Encoding（行程长度压缩算法））
version：v2
time:2020/11/06
author:huangxiaohuang
"""

import json
import os
import shutil

import cv2
from tqdm import tqdm

dataset = {}


# 读取xml文件
def readjson(dataset, json_path, img_name):
    global img_width, img_height
    json_path = json_path.replace('\\', '/')
    print(json_path)
    with open(json_path, 'r', encoding='utf8')as fp:
        json_datas = json.load(fp)
        # print('这是文件中的json数据：', json_datas)
    for json_data in json_datas:
        # print('json_data', json_data)
        x, y, w, h = json_data['x'], json_data['y'], json_data['w'], json_data['h']
        # print('x,y,w,h', x, y, w, h)
        image_path = os.path.join(trainimg + '/' + str(img_name) + '.jpg')
        print('image_path', image_path)
        img = cv2.imread(image_path)
        # img_shape = img.shape[0:2]
        img_width = 1000
        img_height = 1000
        # print('img_width', img_width)
        # print('img_width', img_height)
        # 保存annotations字段
        dataset.setdefault("annotations", []).append({
            'image_id': img_name,
            'bbox': [x, y, w, h],
            'category_id': 1,
            'area': (img_width * img_height),
            'iscrowd': 0,
            'id': img_name,
            'segmentation': []
        })
        #   保存images字段
    dataset.setdefault("images", []).append({
        'file_name': str(img_name) + '.jpg',
        'id': img_name,
        'width': img_width,
        'height': img_height
    })


# 原始图片路径
im_path = "G:/cervical_cancer/code/learn/train/faster-rcnn/model/VOCdevkit/VOC2012/JPEGImages"
# 新产生图片路径
trainimg = "./data/"

img_count = 0
dirpath = os.listdir(im_path)
f1 = os.listdir(im_path)
for file in f1:
    if file.split(".")[1] == "jpg":
        img_count += 1
print(img_count)
for imgdir in tqdm(dirpath):
    count = 1
    for file in tqdm(os.listdir(im_path)):
        img_name = file.split(".")[0]
        print(file.split(".")[0])
        if file.split(".")[1] == "jpg":
            oldname = os.path.join(im_path, file).replace('\\', '/')
            jpgname = os.path.join(trainimg, img_name + ".jpg")
            # 复制图片到新产生图片的路径文件夹
            # shutil.copyfile(oldname, jpgname)
            # 读取相应图片的json文件
            readjson(dataset, os.path.join('./label/',
                                           file.split(".")[0] + ".json"), img_name)
        # count += 1
    break
# 保存categories字段
for i in range(1, 3):
    dataset.setdefault("categories", []).append({
        'id': i - 1,
        'name': 'pos',
        'supercategory': 'pos'
    })
# 产生instances_minival2014.json文件的保存路径
folder = os.path.join('./coco/')
if not os.path.exists(folder):
    os.makedirs(folder)
json_name = os.path.join(folder + 'instances_minival2014.json')
with open(json_name, 'w') as f:
    json.dump(dataset, f)
