import os
from django.conf import settings
from .models import Dog_post

def update_image_path():
    image_models = Dog_post.objects.all()

    for image_model in image_models:
        # 이미지1 경로 업데이트
        old_image_path1 = image_model.image1.name
        filename1 = os.path.basename(old_image_path1)
        new_image_path1 = f'postings/{str(image_model.pk).zfill(5)}/{filename1}'
        image_model.image1.name = new_image_path1

        # 이미지2 경로 업데이트
        old_image_path2 = image_model.image2.name
        filename2 = os.path.basename(old_image_path2)
        new_image_path2 = f'postings/{str(image_model.pk).zfill(5)}/{filename2}'
        image_model.image2.name = new_image_path2

        # 이미지3 경로 업데이트
        old_image_path3 = image_model.image3.name
        filename3 = os.path.basename(old_image_path3)
        new_image_path3 = f'postings/{str(image_model.pk).zfill(5)}/{filename3}'
        image_model.image3.name = new_image_path3

        # 데이터베이스에 변경 사항 저장
        image_model.save(update_fields=['image1', 'image2', 'image3'])

        # 이미지 파일 이동
        old_image_file1 = os.path.join(settings.MEDIA_ROOT, old_image_path1)
        new_image_file1 = os.path.join(settings.MEDIA_ROOT, new_image_path1)
        os.rename(old_image_file1, new_image_file1)

        old_image_file2 = os.path.join(settings.MEDIA_ROOT, old_image_path2)
        new_image_file2 = os.path.join(settings.MEDIA_ROOT, new_image_path2)
        os.rename(old_image_file2, new_image_file2)

        old_image_file3 = os.path.join(settings.MEDIA_ROOT, old_image_path3)
        new_image_file3 = os.path.join(settings.MEDIA_ROOT, new_image_path3)
        os.rename(old_image_file3, new_image_file3)

