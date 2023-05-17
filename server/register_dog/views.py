from django.shortcuts import render, redirect
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