from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'register_dog'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_post/', views.LostCreate.as_view()),


]