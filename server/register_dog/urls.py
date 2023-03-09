from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'register_dog'

urlpatterns = [
    path('', views.index, name='index'),
    path('main2/', views.index2, name='index2'),
    path('create_post_lost/', views.LostCreate.as_view()),
    path('create_post_found/', views.FoundCreate.as_view()),

]