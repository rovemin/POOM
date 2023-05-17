import os

import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from .models import Dog_post, Category
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

    # # 이전 이미지 파일 삭제
    # if instance.pk and created:
    #     old_instance = Dog_post.objects.get(pk=instance.pk)
    #     if old_instance.image1 != instance.image1:
    #         old_image1_path = os.path.join(settings.MEDIA_ROOT, old_instance.image1.name)
    #         if os.path.isfile(old_image1_path):
    #             os.remove(old_image1_path)
    #
    #     if old_instance.image2 != instance.image2:
    #         old_image2_path = os.path.join(settings.MEDIA_ROOT, old_instance.image2.name)
    #         if os.path.isfile(old_image2_path):
    #             os.remove(old_image2_path)
    #
    #     if old_instance.image3 != instance.image3:
    #         old_image3_path = os.path.join(settings.MEDIA_ROOT, old_instance.image3.name)
    #         if os.path.isfile(old_image3_path):
    #             os.remove(old_image3_path)

def mypage(request):
    posts = Dog_post.objects.all()

    return render(
        request,
        'register_dog/mypage.html',
        {
            'posts': posts,
        }
    )

def imageresult(request):
    posts = Dog_post.objects.all()

    return render(
        request,
        'register_dog/imageresult.html',
        {
            'posts': posts,
        }
    )

model = SentenceTransformer("Huffon/sentence-klue-roberta-base")
def textresult(request):
    docs = list(Dog_post.objects.values('description'))
    document_embeddings = model.encode(docs)

    query = request.POST['text_search']
    query_embedding = model.encode(query)

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
'''
def imageresult(request):

    print_result = clustering.py

    return render(
        request,
        'register_dog/imageresult.html',

        {
            'print_result':print_result,
        }
    )
'''

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