from django.shortcuts import render
from utils.tencent.SMS import send_sms_single
from django.http import HttpResponse
import random
from django.conf import settings
# Create your views here.
def send_sms(request):
    """发送短信"""
    code=random.randrange(1000,9999)
    tpl=request.GET.get('tpl')
    template_id=settings.TENCENT_SMS_TEMPLATE[tpl]
    if not template_id:
        return HttpResponse('模板不存在，无法获取模板id')
    res=send_sms_single(phone_num=15667362251,template_id=template_id,template_param_list=[code])
    print(res)
    if res['result']==0:
        return HttpResponse('发送成功')
    else:
        return HttpResponse('发送失败')