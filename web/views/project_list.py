from django.http import JsonResponse
from django.shortcuts import render
from web.forms.project import ProjectMdoelForm
def project_list(request):
    if request.method=='GET':
        form=ProjectMdoelForm(request)
        return render(request,'project_list.html',{'form':form})
    form=ProjectMdoelForm(request,data=request.POST)
    if form.is_valid():
        #验证通过 用户仅提供博客名，风格，描述，还有一些字段尚未给出
        form.instance.creator=request.blog.user
        #创建项目
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status':False,'errors':form.errors})