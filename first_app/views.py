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
        return HttpResponse(res['errmsg'])

from django import forms
from first_app import models
from django.core.validators import RegexValidator


class SignUpModelForm(forms.ModelForm):
    telephone=forms.CharField(label='手机号',validators=[RegexValidator(r'^(1|3|4|5|6|7|8|9)\d{9}$','手机号格式错误'),])
    password=forms.CharField(label='密码',widget=forms.PasswordInput())
    confirm_password=forms.CharField(label='确认密码',widget=forms.PasswordInput())
    verification_code=forms.CharField(label='验证码',widget=forms.TextInput())
    class Meta:
        model=models.UserInfo
        fields=['username','email','password','confirm_password','telephone','verification_code']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,filed in self.fields.items():
            filed.widget.attrs['class']='form-control'
            filed.widget.attrs['placeholder']='请输入'+filed.label

def sign_up(request):
    form=SignUpModelForm()
    return render(request,'sign_up.html',{'form':form})