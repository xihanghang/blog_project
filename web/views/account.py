"""
用户账户相关功能
登录 注册 注销 短信
"""
from django.shortcuts import render
from django.http import HttpResponse
from web.forms.account import  SendSmsForm
from django.http import JsonResponse
from django_redis import get_redis_connection
# Create your views here.
def send_sms(request):
    # """发送短信"""
    # code=random.randrange(1000,9999)
    # tpl=request.GET.get('tpl')
    # template_id=settings.TENCENT_SMS_TEMPLATE[tpl]
    # if not template_id:
    #     return HttpResponse('模板不存在，无法获取模板id')
    # res=send_sms_single(phone_num=15667362251,template_id=template_id,template_param_list=[code])
    # print(res)
    # if res['result']==0:
    #     return HttpResponse('发送成功')
    # else:
    #     return HttpResponse(res['errmsg'])
    form=SendSmsForm(request,data=request.GET)
    if form.is_valid():
        #发送短信redis
        #写入
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})

from web.forms.account import SignUpModelForm

def sign_up(request):
    if request.method=='GET':
        form=SignUpModelForm()
        return render(request,'sign_up.html',{'form':form})
    # print(request.POST)
    form=SignUpModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
    else:
        print(form.errors)
    return JsonResponse({})

