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


# class PostList(ListView):
#     model = Dog_post
#     template_name = 'main1.html'
#     context_object_name = 'dog_post_list'
#     ordering = '-pk'  # 최신글부터 보여줌.
#
#     def get_context_data(self, **kwargs):
#         context = super(PostList, self).get_context_data()
#         context['categories'] = Category.objects.all()
#         return context


# def main1(request):
#     posts = Dog_post.objects.all()
#
#     return render(
#         request,
#         'register_dog/main1.html',
#         {
#             'posts': posts,
#         }
#     )

# 보호자가 실종견 등록
class LostCreate(LoginRequiredMixin, CreateView):
    model = Dog_post
    fields = ['post_title', 'category', 'dog_name', 'breed', 'location_city',
              'location_detail', 'date', 'sex', 'age', 'reward', 'description',
              'image1', 'image2', 'image3']
    template_name = 'register_dog/dog_post_lost_form.html'
    success_url = '/create_post_lost/'

    # def test_func(self):
    #     return self.request.user.is_superuser or self.request.user.is_staff

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
    #label = {
    #
    #    'post_title' : '글 제목*',
    #    'category' : '글 종류',
    #    'breed' : '견종',
    #    'location_city' : '발견된 위치(시/도)*',
    #    'location_detail' : '발견된 위치(구체적인 장소)',
    #    'date' : '발견 날짜(YYYY-MM-DD)*',
    #    'sex' : '성별',
    #    'description' : '기타 특징*',
    #    'image1' : '사진1',
    #    'image2' : '사진2',
    #    'image3' : '사진3'
    #}

    template_name = 'register_dog/dog_post_found_form.html'
    success_url = '/create_post_found/'

    # def test_func(self):
    #     return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(FoundCreate, self).form_valid(form)
        else:
            return redirect('/create_post_found/')

    # def get_category_initial(self):
    #     return {'category':'제보',}

def mypage(request):
    posts = Dog_post.objects.all()

    return render(
        request,
        'register_dog/mypage.html',
        {
            'posts': posts,
        }
    )