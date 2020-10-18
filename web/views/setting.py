from django.shortcuts import render,HttpResponse,redirect
from web import models
from utils.tencent.cos import delete_bucket
def setting(request,project_id):
    return render(request,'setting.html')

def delete(request,project_id):
    if request.method=='GET':
        return render(request,'setting_delete.html')
    project_name=request.POST.get('project_name')
    if not project_name or project_name!=request.blog.project.name:
        return render(request, 'setting_delete.html',{'error':'项目名错误'})
    if request.blog.user!=request.blog.project.creator:
        return render(request, 'setting_delete.html',{'error':'没有权限仅有项目创建者可以删除该项目'})

    #删除桶和删除项目
    delete_bucket(request.blog.project.bucket,request.blog.project.region)
    models.Project.objects.filter(id=project_id,creator=request.blog.project.creator).delete()

    return redirect("project_list")
