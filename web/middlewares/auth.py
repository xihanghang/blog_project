from django.utils.deprecation import MiddlewareMixin
from web import models
from django.shortcuts import redirect
from django.conf import settings
class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        """如果用户已登录，则在request中赋值"""
        user_id=request.session.get('user_id',0)
        user_object=models.UserInfo.objects.filter(id=user_id).first()
        request.blog=user_object

        # 如果访问后台且没有登录重定向到登陆页面 此处需要设置url白名单
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.blog:
            return redirect('sign_in')
        # print(request.path_info)