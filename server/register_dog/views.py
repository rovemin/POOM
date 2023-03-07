from django.shortcuts import render, redirect
from .models import Dog_post, Category
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def index(request):
    posts = Dog_post.objects.all()

    return render(
        request,
        'register_dog/main1.html',
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

class LostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Dog_post
    fields = ['post_title', 'category', 'dog_name', 'breed', 'location_city',
              'location_detail', 'date', 'sex', 'age', 'reward', 'description',
              'image1', 'image2', 'image3']
    success_url = '/create_post/'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(LostCreate, self).form_valid(form)
        else:
            return redirect('/create_post/')
