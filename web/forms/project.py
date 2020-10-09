

from django import forms
from web import models
from web.forms.bootstrap import BootStrap
from django.core.exceptions import ValidationError
class ProjectMdoelForm(BootStrap,forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea())
    class Meta:
        model=models.Project
        fields=['name','color','desc']
        widgets={
            'desc':forms.Textarea
        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request
    def clean_name(self):
        name=self.cleaned_data['name']
        exists=models.Project.objects.filter(name=name,creator=self.request.blog.user).exists()
        if exists:
            raise ValidationError('项目名已存在，请修改')
        #判断当前用户是否还有额度创建项目
        #最多创建N个项目
        #self.request.blog.price_policy.project_num
        #现在已经创建的项目
        count=models.Project.objects.filter(creator=self.request.blog.user).count()
        if count>=self.request.blog.price_policy.project_num:
            raise ValidationError('项目创建个数已达上限，如需继续创建请购买套餐')
        return name
