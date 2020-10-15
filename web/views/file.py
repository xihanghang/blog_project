from django.shortcuts import render
from django.http import JsonResponse
from django.forms import model_to_dict
from web.forms.file import FolderModelForm
from web import models
def file(request,project_id):
    parent_object = None
    folder_id = request.GET.get('folder', '')
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(id=folder_id, file_type=2,
                                                             project=request.blog.project).first()
    #GET请求为查看页面
    if request.method=='GET':

        breadcrumd_list=[]
        parent=parent_object
        while parent:
            # breadcrumd_list.insert(0,{'id':parent.id,'name':parent.name})
            breadcrumd_list.insert(0, model_to_dict(parent,['id','name']))
            parent=parent.parent

        queryset=models.FileRepository.objects.filter(project=request.blog.project,)
        if parent_object:
            #进入某一个目录
            file_object_list=queryset.filter(parent=parent_object).order_by('-file_type')
        else:
            file_object_list=queryset.filter(parent__isnull=True).order_by('-file_type')
            #进入根目录

        form=FolderModelForm(request,parent_object)
        return render(request,'file.html',{'form':form,'file_object_list':file_object_list,'breadcrumd_list':breadcrumd_list})

    fid=request.POST.get('fid','')
    edit_object=None
    if fid.isdecimal():
        edit_object=models.FileRepository.objects.filter(id=int(fid),file_type=2,project=request.blog.project).first()
    if edit_object:
        form=FolderModelForm(request,parent_object,data=request.POST,instance=edit_object)
    else:
        form=FolderModelForm(request,parent_object,request.POST)
    #POST请求为添加文件

    if form.is_valid():
        form.instance.project=request.blog.project
        form.instance.file_type=2
        form.instance.update_user = request.blog.user
        form.instance.parent=parent_object
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status':False,'errors':form.errors})