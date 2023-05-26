import os
import numpy as np
import skimage as sk
import matplotlib.pyplot as plt
import matplotlib.image as img
from tqdm import tqdm_notebook

import requests
import cv2
from sklearn.cluster import KMeans
import tensorflow as tf
import keras
import keras.backend as K
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UploadedImageForm
#from . import clustering
from .models import Dog_post, Category, Uploaded_Image
#from .server.register_dog import forms
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from sentence_transformers import SentenceTransformer, util
import torch


def main1(request):
    posts = Dog_post.objects.filter(category=1)

    return render(
        request,
        'register_dog/main1.html',
        {
            'posts': posts,
        }
    )

def main2(request):
    posts = Dog_post.objects.filter(category=2)

    return render(
        request,
        'register_dog/main2.html',
        {
            'posts': posts,
        }
    )

# 보호자가 실종견 등록
class LostCreate(LoginRequiredMixin, CreateView):
    model = Dog_post

    fields = ['post_title', 'category', 'dog_name', 'breed', 'location_city',
              'location_detail', 'date', 'sex', 'age', 'reward', 'description',
              'image1', 'image2', 'image3']
    template_name = 'register_dog/dog_post_lost_form.html'
    success_url = '/create_post_lost/'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(LostCreate, self).form_valid(form)
        else:
            return redirect('/create_post_lost/')

# 실종견 제보
class FoundCreate(LoginRequiredMixin, CreateView):
    model = Dog_post
    fields = ['post_title', 'category', 'breed', 'location_city',
              'location_detail', 'date', 'sex', 'description',
              'image1', 'image2', 'image3']

    template_name = 'register_dog/dog_post_found_form.html'
    success_url = '/create_post_found/'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(FoundCreate, self).form_valid(form)
        else:
            return redirect('/create_post_found/')

# 이미지 파일 저장 경로 변경
@receiver(post_save, sender=Dog_post)
def update_image_path(sender, instance, created, **kwargs):
    if created:
        if instance.image1:
            image1_path = f'images/{str(instance.pk).zfill(4)}/{instance.image1.name}'
            full_image1_path = os.path.join(settings.MEDIA_ROOT, image1_path)
            os.makedirs(os.path.dirname(full_image1_path), exist_ok=True)
            instance.image1.storage.save(full_image1_path, instance.image1)
            instance.image1.name = image1_path

        if instance.image2:
            image2_path = f'images/{str(instance.pk).zfill(4)}/{instance.image2.name}'
            full_image2_path = os.path.join(settings.MEDIA_ROOT, image2_path)
            os.makedirs(os.path.dirname(full_image2_path), exist_ok=True)
            instance.image2.storage.save(full_image2_path, instance.image2)
            instance.image2.name = image2_path

        if instance.image3:
            image3_path = f'images/{str(instance.pk).zfill(4)}/{instance.image3.name}'
            full_image3_path = os.path.join(settings.MEDIA_ROOT, image3_path)
            os.makedirs(os.path.dirname(full_image3_path), exist_ok=True)
            instance.image3.storage.save(full_image3_path, instance.image3)
            instance.image3.name = image3_path

        instance.save()


def mypage(request):
    posts = Dog_post.objects.all()

    return render(
        request,
        'register_dog/mypage.html',
        {
            'posts': posts,
        }
    )

# Loss definition
alpha = 0.3
def triplet(y_true, y_pred):
    a = y_pred[0::3]
    p = y_pred[1::3]
    n = y_pred[2::3]

    ap = K.sum(K.square(a-p), -1)
    an = K.sum(K.square(a-n), -1)

    return K.sum(tf.nn.relu(ap-an+alpha))
# Metric definition
def triplet_acc(y_true, y_pred):
    a = y_pred[0::3]
    p = y_pred[1::3]
    n = y_pred[2::3]

    ap = K.sum(K.square(a - p), -1)
    an = K.sum(K.square(a - n), -1)

    return K.less(ap+alpha, an)


def imageresult(request):
    if (request.method == 'POST'):
        uploaded_image_model = Uploaded_Image()
        uploaded_image_model.uploaded_image = request.FILES.get('image_upload')
        uploaded_image_model.save()

    PATH = 'C:\\rovemin\\POOM\\server\\media\\images'
    filenames = []
    labels = []
    idx = 0
    SIZE = (224,224,3)

    for path, dirs, files in os.walk(PATH):
        if len(files) > 0:
            if len(files) > 0:
                for file in files:
                    file_path = os.path.join(path, file)
                    filenames.append(file_path)
            labels = np.append(labels, np.ones(len(files))*idx)
            idx += 1

    h, w, c = SIZE
    images = np.empty((len(filenames), h, w, c))
    for i, f in enumerate(filenames):
        images[i] = sk.io.imread(f)

    # Normalization
    images /= 255.0

    # 게시물 폴더 개수
    nbof_classes = len(np.unique(labels))

    # loss definition
    alpha = 0.3

    def triplet(y_true, y_pred):

        a = y_pred[0::3]
        p = y_pred[1::3]
        n = y_pred[2::3]

        ap = K.sum(K.square(a - p), -1)
        an = K.sum(K.square(a - n), -1)

        return K.sum(tf.nn.relu(ap - an + alpha))

    # metric definition
    def triplet_acc(y_true, y_pred):
        a = y_pred[0::3]
        p = y_pred[1::3]
        n = y_pred[2::3]

        ap = K.sum(K.square(a - p), -1)
        an = K.sum(K.square(a - n), -1)

        return K.less(ap + alpha, an)

    # 모델 정의
    model = tf.keras.models.load_model('C:\\rovemin\\POOM\\server\\model\\2023.04.30.dogfacenet.146.h5',
                                       custom_objects={'triplet': triplet, 'triplet_acc': triplet_acc})

    mod = tf.keras.Model(model.layers[0].input, model.layers[-1].output)
    predict = mod.predict(images)
    kmeans = KMeans(n_clusters=len(np.unique(labels)), max_iter=2000, random_state=0, tol=0.2).fit(predict)

    images_cluster = [images[np.equal(kmeans.labels_, i)] for i in range(len(labels))]
    labels_cluster = [labels[np.equal(kmeans.labels_, i)] for i in range(len(labels))]

    # 임시로 input 이미지 지정해서 시험해보기
    input_image = 'POOM/server/media/images/0000/img1.jpg'
    input_image_split = input_image.split('/')
    input_image_folder = int(input_image_split[4])

    clustering_num = []

    for i in range(len(labels_cluster)):
        if input_image_folder in labels_cluster[i]:
            clustering_num.append(i)


    # for i in range(len(clustering_num)):
    #     length = len(images_cluster[clustering_num[i]])
    #     if length > 0:
    #         print(labels_cluster[clustering_num[i]])
    #         fig = plt.figure(figsize=(length * 2, 2))
    #         for j in range(length):
    #             picture = img.imread(images_cluster[clustering_num[i]][j])
    #             picture = plt.imshow(picture)
    #             picture = plt.show()

    # picture = img.imread(labels_cluster[1][1])
    # picture = plt.imshow(picture)

    return render(
        request,
        'register_dog/imageresult.html',
        {
            # 'input_image_folder':input_image_folder,
            # 'filenames':filenames,
            # 'labels': labels,
            # 'picture':labels_cluster[0],
            # 'num': clustering_num,
            # 'input_image': input_image,
            'clustering_num': clustering_num.append(i)

        }
    )



model2 = SentenceTransformer("Huffon/sentence-klue-roberta-base")
def textresult(request):
    docs = list(Dog_post.objects.values('description'))
    document_embeddings = model2.encode(docs)

    query = request.POST['text_search']
    query_embedding = model2.encode(query)

    top_k = min(5, len(docs))

    # 입력 문장 - 문장 후보군 간 코사인 유사도 계산
    cos_scores = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]
    # 코사인 유사도 순으로 'top_k' 개 문장 추출
    top_results = torch.topk(cos_scores, k=top_k)
    results = []
    results_idx = []

    numbers = []

    # result = enumerate(zip(top_results[0], top_results[1]))
    for i, (score, idx) in enumerate(zip(top_results[0], top_results[1])):
        result = docs[idx]

        results_idx.append(idx.item()+1)
        results.append(result['description'])

    print_result = list(zip(results_idx, results))

    for i in range(top_k):
        numbers.append(i)

    return render(
        request,
        'register_dog/textresult.html',

        {

            'print_result':print_result,

        }
    )

def detail(request, pk):
    post = Dog_post.objects.get(pk=pk)

    context = {'post': post}

    return render(
        request,
        'register_dog/detail.html',
        context
     )

def mypage(request):
    # logged_in_user = request.user
    logged_in_user_posts = Dog_post.objects.filter(author=request.user)
    return render(
        request,
        'register_dog/mypage.html',
        {
            'posts':logged_in_user_posts,
        }
    )