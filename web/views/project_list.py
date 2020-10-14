from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect
from web.forms.project import ProjectMdoelForm
from web import models
from utils.tencent.cos import create_bucket
import time
def project_list(request):
    if request.method=='GET':
        """
        从数据库获取两部分数据
        我创建的所有项目：已星标，未星标
        我参与的所有项目：已星标，未星标
        
        提取已星标
        
        将得到三个列表
        """
        project_dict={'star':[],'my':[],'join':[]}

        my_project_list=models.Project.objects.filter(creator=request.blog.user)
        for row in  my_project_list:
            if row.star:
                project_dict['star'].append({'value':row,'type':'my'})
            else:
                project_dict['my'].append(row)
        join_project_list=models.ProjectUser.objects.filter(user=request.blog.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value':item.project,'type':'join'})
            else:
                project_dict['join'].append(item.project)
        form=ProjectMdoelForm(request)
        return render(request,'project_list.html',{'form':form,'project_dict':project_dict})
    form=ProjectMdoelForm(request,data=request.POST)
    if form.is_valid():
        #为项目创建cos桶
        #构建唯一桶名称手机号，时间
        bucket="{}-{}-1303841926".format(request.blog.user.mobile_phone,str(int(time.time())))
        region="ap-chengdu"
        create_bucket(bucket,region)
        #将桶和区域存储
        form.instance.bucket=bucket
        form.instance.region=region
        #验证通过 用户仅提供博客名，风格，描述，还有一些字段尚未给出
        form.instance.creator=request.blog.user
        #创建项目
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status':False,'errors':form.errors})

def project_star(request,project_type,project_id):

    """星标项目"""

    if project_type=='my':
        models.Project.objects.filter(id=project_id,creator=request.blog.user).update(star=True)
        return redirect('project_list')
    if project_type=='join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.blog.user).update(star=True)
        return redirect('project_list')
    return HttpResponse('请求错误')

def project_unstar(request,project_type,project_id):
    """取消星标"""
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.blog.user).update(star=False)
        return redirect('project_list')
    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.blog.user).update(star=False)
        return redirect('project_list')
    return HttpResponse('请求错误')