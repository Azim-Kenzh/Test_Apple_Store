from django import forms
from django.forms import modelformset_factory

from .models import *


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )


ImagesFormSet = modelformset_factory(Image, form=ImageForm, extra=3  ,max_num=4,  can_delete=True)


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text', ]

    def save(self, commit=False):
        self.Meta.model.save()

