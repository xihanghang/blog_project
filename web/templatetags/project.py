from django.template import Library
from web import models
from django.urls import reverse
register=Library()

@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    #获取我创建的
    my_project_list=models.Project.objects.filter(creator=request.blog.user)
    #获取我参与的
    join_project_list=models.ProjectUser.objects.filter(user=request.blog.user)
    return {'my':my_project_list,'join':join_project_list,'request':request}

@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    data_list=[
        {'title': '概述', 'url': reverse('dashboard', kwargs={'project_id': request.blog.project.id})},
        {'title': '问题', 'url': reverse('issues', kwargs={'project_id': request.blog.project.id})},
        {'title': '文件', 'url': reverse('file', kwargs={'project_id': request.blog.project.id})},
        {'title': '统计', 'url': reverse('statistic', kwargs={'project_id': request.blog.project.id})},
        {'title': 'wiki', 'url': reverse('wiki', kwargs={'project_id': request.blog.project.id})},
        {'title': '设置', 'url': reverse('setting', kwargs={'project_id': request.blog.project.id})},
    ]
    for item in data_list:
        if request.path_info.startswith(item['url']):
            item['class']='active'
    return {'data_list':data_list}