

from web import models
from django import forms
from web.forms.bootstrap import BootStrap

class WikiModelForm(BootStrap,forms.ModelForm):

    class Meta:
        model=models.Wiki
        exclude=['project','depth']
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #找到想要的字段把他绑定显示的数据重置
        #数据=去数据库获取的当前项目所有Wiki标题
        total_list=[("","请选择")]
        data_list=models.Wiki.objects.filter(project=request.blog.project).values_list('id','title')
        total_list.extend(data_list)
        self.fields['parent'].choices=total_list