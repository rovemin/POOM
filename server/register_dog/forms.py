from django import forms

from .models import Uploaded_Image


class UploadedImageForm(forms.ModelForm):
    class Meta:
        model = Uploaded_Image
        fields = ['uploaded_image']
        labels = {
            'uploaded_image' : '이미지 업로드'
        }
        