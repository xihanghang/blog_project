
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.tencent.SMS import send_sms_single
import random
from django_redis import get_redis_connection
from utils.encrypt import MD5
from web.forms.bootstrap import BootStrap
class SignUpModelForm(BootStrap,forms.ModelForm):

    mobile_phone=forms.CharField(label='手机号',validators=[RegexValidator(r'^(1|3|4|5|6|7|8|9)\d{10}$','手机号格式错误'),])
    password=forms.CharField(label='密码',widget=forms.PasswordInput(),min_length=8,max_length=32,error_messages={'min_length':'密码不能少于八位','max_length':'密码不能超过十六位'})
    confirm_password=forms.CharField(label='确认密码',widget=forms.PasswordInput(),min_length=8,max_length=16,error_messages={'min_length':'确认密码不能少于八位','max_length':'确认密码不能超过十六位'})
    verification_code=forms.CharField(label='验证码',widget=forms.TextInput())
    class Meta:
        model=models.UserInfo
        fields=['username','email','password','confirm_password','mobile_phone','verification_code']
    def clean_username(self):
        username=self.cleaned_data['username']
        exist=models.UserInfo.objects.filter(username=username).exists()
        if exist:
            raise ValidationError('该用户已存在')
        #   self.add_error('username','用户名不存在ai')
        return username
    def clean_email(self):
        email=self.cleaned_data['email']
        exists=models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('该邮箱已被注册')
        return email
    def clean_password(self):
        password = MD5(self.cleaned_data.get('password'))
        return password
    def clean_confirm_password(self):
        password=self.cleaned_data.get('password')
        confirm_password=MD5(self.cleaned_data['confirm_password'])
        if password!=confirm_password:
            raise ValidationError('两次密码输入不一致')
        return confirm_password
    def clean_mobile_phone(self):
        mobile_phone=self.cleaned_data['mobile_phone']
        exists=models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('该手机号已被注册')
        return mobile_phone
    def clean_verification_code(self):
        code=self.cleaned_data['verification_code']
        mobile_phone=self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code
        conn=get_redis_connection()
        code_1=conn.get(mobile_phone)
        if not code_1:
            raise ValidationError('失效的验证码，请重新发送')
        code_1=code_1.decode('utf-8')
        if code.strip()!=code_1:
            raise ValidationError('验证码输入有误')
        return code


class SignInModelForm(BootStrap,forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1|3|4|5|6|7|8|9)\d{10}$', '手机号格式错误'), ])
    verification_code=forms.CharField(label='验证码',widget=forms.TextInput())
    def clean_mobile_phone(self):
        mobile_phone=self.cleaned_data['mobile_phone']
        user_object=models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        if not user_object:
            raise ValidationError('手机号不存在请先注册')
        return user_object
    def clean_verification_code(self):
        user_object=self.cleaned_data.get('mobile_phone')
        code=self.cleaned_data['verification_code']
        if not user_object:
            return code
        conn = get_redis_connection()
        redis_code = conn.get(user_object.mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')
        redis_str_code=redis_code.decode('utf-8')
        if code.strip()!=redis_str_code:
            raise ValidationError('验证码输入错误，请重新输入')
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
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl=='sign_in_sms':
            if not exists:
                raise ValidationError('手机号不存在请先注册')
        else:
            if exists:
                raise ValidationError('该手机号已经注册过')
        #发送短信&存入redis
        code=random.randrange(1000,9999)
        #发送短信
        sms=send_sms_single(mobile_phone,template_id,[code])
        if sms['result']!=0:
            raise ValidationError('短信发送失败：{}'.format(sms['errmsg']))
        #将验证码写入redis（利用django-redis组件）
        conn=get_redis_connection()
        conn.set(mobile_phone,code,ex=1000)
        # conn.get(mobile_phone)
        return mobile_phone

class Signin(BootStrap,forms.Form):
    username=forms.CharField(label='邮箱或手机号')
    password=forms.CharField(label='密码',widget=forms.PasswordInput())#render_value=True表示在前端登陆页面刷新时密码框不会清空
    code=forms.CharField(label='图片验证码')
    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request=request
    def clean_password(self):
        password = MD5(self.cleaned_data.get('password'))
        return password
    def clean_code(self):
        """钩子函数 读取验证码 并进行校验"""
        code=self.cleaned_data['code']
        #获取session中的code
        session_code=self.request.session.get('image_code')
        if not session_code:
            return ValidationError('验证码已过期')
        if code.strip().upper() != session_code.strip().upper():
            return ValidationError('验证码输入错误')
        return code