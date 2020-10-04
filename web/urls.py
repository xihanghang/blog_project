
from django.conf.urls import url
from web.views import account,SMS


urlpatterns=[
    url(r'^sign_up/',account.sign_up,name='sign_up'),
    url(r'^send_sms/',SMS.send_sms_single,name='send_sms')
]