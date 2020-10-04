
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.tencent.SMS import send_sms_single
import random
from django_redis import get_redis_connection
class SignUpModelForm(forms.ModelForm):

    mobile_phone=forms.CharField(label='手机号',validators=[RegexValidator(r'^(1|3|4|5|6|7|8|9)\d{10}$','手机号格式错误'),])
    password=forms.CharField(label='密码',widget=forms.PasswordInput(),min_length=8,max_length=16,error_messages={'min_length':'密码不能少于八位','max_length':'密码不能超过十六位'})
    confirm_password=forms.CharField(label='确认密码',widget=forms.PasswordInput(),min_length=8,max_length=16,error_messages={'min_length':'确认密码不能少于八位','max_length':'确认密码不能超过十六位'})
    verification_code=forms.CharField(label='验证码',widget=forms.TextInput())
    class Meta:
        model=models.UserInfo
        fields=['username','email','password','confirm_password','mobile_phone','verification_code']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,filed in self.fields.items():
            filed.widget.attrs['class']='form-control'
            filed.widget.attrs['placeholder']='请输入'+filed.label
    def clean_username(self):
        username=self.cleaned_data['username']
        exist=models.UserInfo.objects.filter(username=username).exists()
        if exist:
            raise ValidationError('该用户已存在')
        return username
    def clean_email(self):
        email=self.cleaned_data['email']
        exists=models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('该邮箱已被注册')
        return email
    def clean_confirm_password(self):
        password=self.cleaned_data['password']
        confirm_password=self.cleaned_data['confirm_password']
        if password!=confirm_password:
            raise ValidationError('两次密码输入不一致')
        return password
    def clean_mobile_phone(self):
        mobile_phone=self.cleaned_data['mobile_phone']
        exists=models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('该手机号已被注册')
        return mobile_phone
    def clean_verification_code(self):
        code=self.cleaned_data['verification_code']
        mobile_phone=self.cleaned_data['mobile_phone']
        conn=get_redis_connection()
        code_1=conn.get(mobile_phone)
        if not code_1:
            raise ValidationError('失效的验证码，请重新发送')
        code_1=code_1.decode('utf-8')
        if code.strip()!=code_1:
            raise ValidationError('验证码输入有误')
        return code

class SendSmsForm(forms.Form):

    mobile_phone=forms.CharField(label='手机号',validators=[RegexValidator(r'^(1|3|4|5|6|7|8|9)\d{10}$','手机号格式错误')])
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request
    def clean_mobile_phone(self):
        #钩子函数
        mobile_phone=self.cleaned_data['mobile_phone']
        tpl=self.request.GET.get('tpl')
        template_id=settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError('短信模板错误')
        exists=models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('该手机号已经注册过')
        #发送短信&存入redis
        code=random.randrange(1000,9999)
        #发送短信
        sms=send_sms_single(mobile_phone,template_id,[code])
        if sms['result']!=0:
            print(sms)
            raise ValidationError('短信发送失败：{}'.format(sms['errmsg']))
        #将验证码写入redis（利用django-redis组件）
        conn=get_redis_connection()
        conn.set(mobile_phone,code,ex=60)
        # conn.get(mobile_phone)
        return mobile_phone
