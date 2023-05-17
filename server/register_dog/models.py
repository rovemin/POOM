import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from PIL import Image
import os

class Category(models.Model):
    category_choices = (('등록', '실종견 등록'), ('제보', '목격/구조 제보'))
    category_name = models.CharField('카테고리(등록/제보)*', max_length=15, unique=True, choices=category_choices)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'


#def get_image_path(instance, filename):
#    return f'../media/images/{instance.pk}/{filename}'

class Dog_post(models.Model):
    post_title = models.CharField('글 제목*', max_length=100, default='')

    category = models.ForeignKey(Category, verbose_name='카테고리(등록/제보)*', on_delete=models.CASCADE)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    dog_name = models.CharField('실종견 이름', max_length=15, null=True, blank=True)
    breed = models.CharField('견종', max_length=40, null=True, blank=True)

    location_city_choices = (('서울', '서울특별시'), ('부산', '부산광역시'),
                             ('대구', '대구광역시'), ('인천', '인천광역시'),
                             ('광주', '광주광역시'), ('대전', '대전광역시'),
                             ('울산', '울산광역시'), ('경기', '경기도'),
                             ('강원', '강원도'), ('충북', '충청북도'),
                             ('충남', '충청남도'), ('전북', '전라북도'),
                             ('전남', '전라남도'), ('경북', '경상북도'),
                             ('경남', '경상남도'), ('세종', '세종특별자치시'),
                             ('제주', '제주특별자치도'))
    location_city = models.CharField('위치(시/도)*', max_length=10, choices=location_city_choices)

    location_detail = models.CharField('위치(세부 설명)', max_length=100, null=True, blank=True)
    date = models.DateField('날짜(YYYY-MM-DD)*', default=datetime.datetime.now())

    sex_choices = (('암컷', '암컷'), ('수컷', '수컷'), ('모름', '모름'))
    sex = models.CharField('성별', max_length=10, null=True, blank=True, choices=sex_choices)

    age = models.CharField('나이', max_length=10, null=True, blank=True)
    reward = models.CharField('사례금', max_length=20, null=True, blank=True)

    description = models.CharField('기타 특징*', max_length=300, default='')

    image1 = models.ImageField('사진1', upload_to='images/', null=True, blank=True)
    image2 = models.ImageField('사진2', upload_to='images/', null=True, blank=True)
    image3 = models.ImageField('사진3', upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.post_title} :: {self.category}'

    def get_ablolute_url(self):
        return '/post/{}/'.format(self.pk)




