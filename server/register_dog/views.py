from django.shortcuts import render
from .models import Dog_post

def index(request):
    posts = Dog_post.objects.all()

    return render(
        request,
        'register_dog/index.html',
        {
            'posts': posts,
        }
    )
