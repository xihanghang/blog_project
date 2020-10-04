
from django import forms
from web import models
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
