from django.db import models

# class Dog_info(models.Model):
#     #회원 아이디 User 나중에 FK로 사용
#     dog_name = models.CharField(max_length=15, null=True)
#     breed = models.CharField(max_length=40, null=True)
#     location_city = models.CharField(max_length=10)
#     location_detail = models.CharField(max_length=100, null=True)
#     date = models.DateTimeField()
#     sex = models.CharField(max_length=10, null=True)
#     age = models.CharField(max_length=10, null=True)
#     reward = models.CharField(max_length=20, null=True)

# class Dog_image(models.Model):
#     # 회원 아이디 User 나중에 FK로 사용
#     image1 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', null=True)
#     image2 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', null=True)
#     image3 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', null=True)

# class Dog_text(models.Model):
#     # 회원 아이디 User 나중에 FK로 사용
#     description = models.CharField(max_length=300)

class Category(models.Model):
    category_name = models.CharField(max_length=15, unique=True)
    def __str__(self):
        return self.category_name

class Dog_post(models.Model):
    dog_name = models.CharField(max_length=15, null=True)

    image1 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', null=True)
    image2 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', null=True)
    image3 = models.ImageField(upload_to='blog/images/%Y/%m/%d/', null=True)

    breed = models.CharField(max_length=40, null=True)
    location_city = models.CharField(max_length=10, default='')
    location_detail = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(null=True)
    sex = models.CharField(max_length=10, null=True)
    age = models.CharField(max_length=10, null=True)
    reward = models.CharField(max_length=20, null=True)

    description = models.CharField(max_length=300, default='')

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

