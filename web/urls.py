
from django.conf.urls import url
from web.views import account
from web.views import home
urlpatterns=[
    url(r'^sign_up/',account.sign_up,name='sign_up'),
    url(r'^send_sms/',account.send_sms,name='send_sms'),
    url(r'^sign_in/sms',account.sign_in_sms,name='sign_in_sms'),
    url(r'^sign_in',account.sign_in,name='sign_in'),
    url(r'^image/code',account.image_code,name='image_code'),
    url(r'^index',home.index,name='index'),
    url(r'^signout/',account.signout,name='signout'),

]