from django.shortcuts import render
from django.http import JsonResponse
from django.forms import model_to_dict
from web.forms.file import FolderModelForm
from web import models
from utils.tencent.cos import delete_file
from utils.tencent.cos import delete_file_list
#http://127.0.0.1:8888/web/manage/1/file/
#http://127.0.0.1:8888/web/manage/1/file/?folder=1
#用户所发请求
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


#http://127.0.0.1:8888/web/manage/1/file/?folder=1
#用户所发请求
def file_delete(request,project_id):
    """删除文件"""
    fid=request.GET.get('fid')
    #级连删除(仅删除了数据库文件)
    delete_object=models.FileRepository.objects.filter(id=fid,project=request.blog.project).first()
    print(delete_object)
    if delete_object.file_type==1:
        #删除文件（数据库文件删除，cos文件删除，返回使用空间）
        #删除文件，将容量返回给当前项目已使用空间
        request.blog.project.user_space-=delete_object.file_size
        request.blog.project.save()
        #cos删除文件
        delete_file(request.blog.project.bucket,request.blog.project.region,delete_object.key)
        #zai数据库删除当前文件
        delete_object.delete()
        return JsonResponse({'status': True})


    total_size=0
    key_list=[]

    folder_list=[delete_object,]
    for folder in folder_list:
        child_list=models.FileRepository.objects.filter(project=request.blog.project,parent=folder).order_by('-file_type')
        for child in child_list:
            if child.file_type==2:
                folder_list.append(child)
            else:
                total_size+=child.file_size
                key_list.append({"Key":child.key})
    if key_list:
        delete_file_list(request.blog.project.bucket,request.blog.project.region,key_list)
    if total_size:
        request.blog.project.user_space -= total_size
        request.blog.project.save()
    delete_object.delete()


