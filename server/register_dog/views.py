from django.shortcuts import render, redirect
from .models import Dog_post, Category
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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

def textresult(request):
    posts = Dog_post.objects.all()

    return render(
        request,
        'register_dog/textresult.html',
        {
            'posts': posts,
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
