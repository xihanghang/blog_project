from django.utils.deprecation import MiddlewareMixin
from web import models
from django.shortcuts import redirect
from django.conf import settings
import datetime


class blog:
    def __init__(self):
        self.user=None
        self.price_policy=None
        self.project=None
class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        """如果用户已登录，则在request中赋值"""
        request.blog=blog()
        user_id=request.session.get('user_id',0)
        user_object=models.UserInfo.objects.filter(id=user_id).first()
        request.blog.user=user_object
        # 如果访问后台且没有登录重定向到登陆页面 此处需要设置url白名单
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.blog.user:
            return redirect('sign_in')
        # print(request.path_info)

        """
        方式一
        如果登陆成功则在后台获取用户最新的交易记录
        将免费额度储存在交易记录中
        """
        # #获取当前用户id值最大的交易记录（最近的一次交易记录）
        # _object=models.Transaction.objects.filter(user=user_object,status=2).order_by('-id').first()
        # #判断是否已经过期
        # current_datetime=datetime.datetime.now()
        # if _object.end_datetime and _object.end_datetime<current_datetime:
        #     _object=models.Transaction.objects.filter(user=user_object,status=2,price_policy_category=1).first()
        # request.blog.price_policy=_object.price_policy

        """
        方式二
        免费的额度存储在配置文件
        """
        #获取当前用户id最大值（最近交易记录)
        _object=models.Transaction.objects.filter(user_id=user_object,status=2).order_by('-id').first()
        if not _object:
            #没有购买
            request.blog.price_policy=models.PricePolicy.objects.filter(category=1,title='个人免费版').first()
        else:
            #付费版
            current_datetime=datetime.datetime.now()
            if _object.end_datetime and _object.end_datetime < current_datetime:
                request.blog.price_policy=models.PricePolicy.objects.filter(category=1,title='个人免费版').first()
            else:
                request.price_policy=_object.price_policy

    def process_view(self,request,view,args,kwargs):
        #判断url是否以manage开头·
        if not request.path_info.startswith('/web/manage/'):
            print('****')
            return
        project_id=kwargs.get('project_id')
        #判断是否是我创建的
        project_object=models.Project.objects.filter(creator=request.blog.user,id=project_id).first()
        if project_object:
            request.blog.project=project_object
            return
        #判断是否是我参与的
        project_user_object=models.ProjectUser.objects.filter(user=request.blog.user,project_id=project_id).first()
        if project_user_object:
            request.blog.project = project_user_object.project
            return

        return redirect('project_list')