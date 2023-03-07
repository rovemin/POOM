# class Dog_post(models.Model):
#     category_name = models.CharField(max_length=15)
#     dog_name = models.CharField(max_length=15, blank=True)
#     breed = models.CharField(max_length=40, blank=True)
#     location_city = models.CharField(max_length=10)
#     location_detail = models.TextField(max_length=100, blank=True)
#     date = models.DateField()
#     sex = models.CharField(max_length=10, blank=True)
#     age = models.CharField(max_length=10, blank=True)
#     reward = models.CharField(max_length=20, blank=True)
#     description = models.TextField(max_length=300)
#     image1 = models.FileField(upload_to='images/', blank=True)
#     image2 = models.FileField(upload_to='images/', blank=True)
#     image3 = models.FileField(upload_to='images/', blank=True)

from django.db import models


class Category(models.Model):
    category_choices = (('등록', '실종견 등록'), ('제보', '목격/구조 제보'))
    category_name = models.CharField(max_length=15, unique=True, choices=category_choices)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'


class Dog_post(models.Model):
    post_title = models.CharField(max_length=100, default='')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')  # 폼에 따라 default 값 설정, 유저 입력 X

    dog_name = models.CharField(max_length=15, null=True, blank=True)
    breed = models.CharField(max_length=40, null=True, blank=True)

    location_city_choices = (('서울', '서울특별시'), ('부산', '부산광역시'),
                             ('대구', '대구광역시'), ('인천', '인천광역시'),
                             ('광주', '광주광역시'), ('대전', '대전광역시'),
                             ('울산', '울산광역시'), ('경기', '경기도'),
                             ('강원', '강원도'), ('충북', '충청북도'),
                             ('충남', '충청남도'), ('전북', '전라북도'),
                             ('전남', '전라남도'), ('경북', '경상북도'),
                             ('경남', '경상남도'), ('세종', '세종특별자치시'),
                             ('제주', '제주특별자치도'))
    location_city = models.CharField(max_length=10, default='시/도 선택', choices=location_city_choices)

    location_detail = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()

    sex_choices = (('암컷', '암컷'), ('수컷', '수컷'), ('모름', '모름'))
    sex = models.CharField(max_length=10, null=True, blank=True, choices=sex_choices)

    age = models.CharField(max_length=10, null=True, blank=True)
    reward = models.CharField(max_length=20, null=True, blank=True)

    description = models.CharField(max_length=300, default='')

    image1 = models.ImageField(upload_to='register_dog/images/%Y/%m/%d/', null=True, blank=True)  # 헤드 이미지
    image2 = models.ImageField(upload_to='register_dog/images/%Y/%m/%d/', null=True, blank=True)
    image3 = models.ImageField(upload_to='register_dog/images/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f'{self.dog_name} :: {self.category}'

    def get_ablolute_url(self):
        return '/post/{}/'.format(self.pk)
