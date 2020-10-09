"""
用户账户相关功能
登录 注册 注销 短信
"""
from django.shortcuts import render,redirect
from django.http import HttpResponse
from web.forms.account import  SendSmsForm
from django.http import JsonResponse
from web import models
import uuid
import datetime
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

from web.forms.account import SignUpModelForm,SignInModelForm,Signin

def sign_up(request):
    if request.method=='GET':
        form=SignUpModelForm()
        return render(request,'sign_up.html',{'form':form})
    # print(request.POST)
    form=SignUpModelForm(data=request.POST)
    if form.is_valid():
        #验证通过并且密码是密文
        instance=form.save()
        #为用户设置默认交易记录
        policy_object=models.PricePolicy.objects.filter(category=1,title='个人免费版').first()
        # models.Transaction.objects.create(
        #     status=2,
        #     order=str(uuid.uuid4()),
        #     user=instance,
        #     price_policy=policy_object,
        #     count=0,
        #     price=0,
        #     start_datetime=datetime.datetime.now()
        # )
        return JsonResponse({'status':True,'data':'/web/sign_in/'})
    return JsonResponse({'status':False,'errors':form.errors})
def sign_in_sms(request):
    if request.method=='GET':
        form=SignInModelForm()
        return render(request, 'sign_in_sms.html', {'form':form})
    form=SignInModelForm(request.POST)
    if form.is_valid():
        #用户输入正确,登陆成功
        mobile_phone=form.cleaned_data['mobile_phone']
        #将用户信息放入session中
        user_object=models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        request.session['user_id']=user_object.id
        request.session.set_expiry(60*60*24*14)
        return JsonResponse({'status':True,'data':'/index/'})
    return JsonResponse({'status': False, 'errors': form.errors})
    # else:
    #     return render(request,'sign_in_sms.html',{'errors':form.errors})

def sign_in(request):
    """
    用户名密码登录
    :param request:
    :return:
    """
    if request.method=='GET':
        form=Signin(request)
        return render(request,'sign_in.html',{'form':form})
    form=Signin(request,data=request.POST)
    if form.is_valid():
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        from django.db.models import Q
        user_object=models.UserInfo.objects.filter(Q(email=username)|Q(mobile_phone=username)).filter(password=password).first()
        if user_object:
            request.session['user_id']=user_object.id
            request.session.set_expiry(60*60*24*14)
            return redirect('index')
        form.add_error('username','账号信息或密码错误')
    return render(request,'sign_in.html',{'form':form})


def image_code(request):
    """图片验证码"""
    from utils.image_code import check_code
    from io import BytesIO
    image_object,code=check_code()
    request.session['image_code']=code
    request.session.set_expiry(180)#主动修改session内容过期时间
    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())

def signout(request):
    request.session.flush()
    return redirect('index')
