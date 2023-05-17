from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

import os
import numpy as np
import skimage as sk
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
import tensorflow.keras.backend as K

from PIL import Image
import cv2

# ----------------------------------------------------------------------------

PATH = '/content/drive/MyDrive/data/dogfacenet'
PATH_MODEL = '/content/drive/MyDrive/data/model'
SIZE = (224,224,3)
VALID_SPLIT = 0.1
TEST_SPLIT = 0.1

# ----------------------------------------------------------------------------
# 데이터셋 내의 이미지 파일 불러와서 resize
import os
import glob
from PIL import Image
from keras.utils import img_to_array

for i in range(0, 297):  # [수정] for i in range file_paths:
    imglist = glob.glob(f'/content/drive/MyDrive/data/dogfacenet/{i}/*.jpg')  # [수정] /_media/register_dog/images/*.jpg

    for img_path in imglist:
        img = Image.open(img_path)
        img.resize((224, 224)).save(img_path)  # 동일한 파일명으로 치환된다.
        np_img = img_to_array(img)
        # print(np_img.shape)

    for img_path in imglist:
        img = Image.open(img_path)
        img.resize((224, 224)).save(img_path)  # 동일한 파일명으로 치환된다.
        np_img = img_to_array(img)
        # print(np_img.shape)

# ----------------------------------------------------------------------------
# 데이터 전처리
import os

filenames = []
labels = []
idx = 0

for path, dirs, files in os.walk(PATH):
  # print(path)
  if len(files) > 0:
    for file in files:
      file_path = os.path.join(path, file)
      filenames.append(file_path)
    labels = np.append(labels, np.ones(len(files))*idx)
    idx += 1
  else:
    print("사진이 존재하지 않아 이미지 검색이 불가능합니다.")

filenames.sort()

# for i in range (len(filenames)):
#   print(filenames[i])

# print(len(labels))
# print(filenames)
h,w,c = SIZE
images = np.empty((len(filenames),h,w,c))
for i,f in enumerate(filenames):
    images[i] = sk.io.imread(f)

images /= 255.0     # Normalization

nbof_classes = len(np.unique(labels))
# print(nbof_classes)

# ----------------------------------------------------------------------------
# Loss Definition
alpha = 0.3
def triplet(y_true, y_pred):
    a = y_pred[0::3]
    p = y_pred[1::3]
    n = y_pred[2::3]

    ap = K.sum(K.square(a - p), -1)
    an = K.sum(K.square(a - n), -1)

    return K.sum(tf.nn.relu(ap - an + alpha))

# ----------------------------------------------------------------------------
# Metric Definition
def triplet_acc(y_true, y_pred):
    a = y_pred[0::3]
    p = y_pred[1::3]
    n = y_pred[2::3]

    ap = K.sum(K.square(a - p), -1)
    an = K.sum(K.square(a - n), -1)

    return K.less(ap + alpha, an)

# ----------------------------------------------------------------------------
# Model Definition
model = tf.keras.models.load_model('/content/drive/MyDrive/data/model/2023.04.06.dogfacenet.109.h5', custom_objects={'triplet':triplet,'triplet_acc':triplet_acc})

# ----------------------------------------------------------------------------
# DogFaceNet Clustering
from sklearn.cluster import KMeans

mod = tf.keras.Model(model.layers[0].input, model.layers[-1].output)

predict=mod.predict(images)

predict=model.predict(images)

kmeans = KMeans(n_clusters=len(np.unique(labels)),max_iter=2000, random_state=0,tol=0.2).fit(predict)

images_cluster = [images[np.equal(kmeans.labels_,i)] for i in range(len(labels))]
labels_cluster = [labels[np.equal(kmeans.labels_,i)] for i in range(len(labels))]

for i in range(len(images_cluster)):
    length = len(images_cluster[i])
    if length > 0:
        # print(labels_cluster[i])
        fig=plt.figure(figsize=(length*2,2))
        for j in range(length):
            plt.subplot(1,length,j+1)
            plt.imshow(images_cluster[i][j])
            plt.xticks([])
            plt.yticks([])
        # plt.show()

# ----------------------------------------------------------------------------
# Input 이미지에 대한 클러스터링 결과 도출

# input 이미지 경로 설정
input_image = '/content/drive/MyDrive/data/dogfacenet/0201/Fd-spclVEAAvwI6.jpg'
input_image_split = input_image.split('/')
input_image_folder = int(input_image_split[6])
print("input image folder number : " + str(input_image_folder))

clustering_num = []

for i in range(len(labels_cluster)):
    if input_image_folder in labels_cluster[i]:
        clustering_num.append(i)

# print(clustering_num)

for i in range(len(clustering_num)):
    length = len(images_cluster[clustering_num[i]])
    if length > 0:
        # print(labels_cluster[clustering_num[i]])
        fig=plt.figure(figsize=(length*2,2))
        for j in range(length):
            # print(j)
            plt.subplot(1,length,j+1)
            plt.imshow(images_cluster[clustering_num[i]][j])
            plt.xticks([])
            plt.yticks([])
        plt.show()
