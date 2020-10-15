from django import forms
from web import models
from web.forms.bootstrap import BootStrap
from django.core.exceptions import ValidationError
class FolderModelForm(BootStrap,forms.ModelForm):
    class Meta:
        model=models.FileRepository
        fields=['name']
    def __init__(self,request,parent_object,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request
        self.parent_object=parent_object

    def clean_name(self):
        name=self.cleaned_data['name']
        # p按段当前目录下此问加减是否存在
        queryset=models.FileRepository.objects.filter(file_type=2, name=name, project=self.request.blog.project)
        if self.parent_object:
            exists=queryset.filter(parent=self.parent_object).exists()

        else:
            exists=queryset.filter(parent__isnull=True).exists()
        if exists:
            raise ValidationError('文件名已存在')
        return name