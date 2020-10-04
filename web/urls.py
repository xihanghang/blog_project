
from django.conf.urls import url
from web.views import account

urlpatterns=[
    url(r'^sign_up/',account.sign_up,name='sign_up'),
    url(r'^send_sms/',account.send_sms,name='send_sms')
]