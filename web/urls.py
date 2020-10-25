
from django.conf.urls import url
from web.views import account
from web.views import home
from web.views import project_list
from django.conf.urls import include
from web.views import manage
from web.views import wiki
from web.views import file
from web.views import setting
from web.views import issues
from web.views import dashboard
from web.views import essay
urlpatterns=[
            url(r'^sign_up/$',account.sign_up,name='sign_up'),
            url(r'^send_sms/$',account.send_sms,name='send_sms'),
            url(r'^sign_in/sms/$',account.sign_in_sms,name='sign_in_sms'),
            url(r'^sign_in/$',account.sign_in,name='sign_in'),
            url(r'^image/code/$',account.image_code,name='image_code'),
            url(r'^index/$',home.index,name='index'),
            url(r'^signout/$',account.signout,name='signout'),
            url(r'^project/list/$',project_list.project_list,name='project_list'),
            url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$',project_list.project_star,name='project_star'),
            url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$',project_list.project_unstar,name='project_unstar'),

            url(r'^price/$', home.price, name='price'),
            url(r'^payment/(?P<policy_id>\d+)/$', home.payment, name='payment'),
            url(r'^pay/$', home.pay, name='pay'),
            url(r'^pay/notify/$', home.pay_notify, name='pay_notify'),

            url(r'^latest/essay/$',essay.latest_essay,name='latest_essay'),

            url(r'^manage/(?P<project_id>\d+)/',include([


                url(r'^statistic/$',manage.statistic,name='statistic'),

                url(r'^wiki/$',wiki.wiki,name='wiki'),
                url(r'^wiki/add/$',wiki.wiki_add,name='wiki_add'),
                url(r'^wiki/catalog/$',wiki.wiki_catalog,name='wiki_catalog'),
                url(r'^wiki/delete/(?P<wiki_id>\d+)$',wiki.wiki_delete,name='wiki_delete'),
                url(r'^wiki/edit/(?P<wiki_id>\d+)$',wiki.wiki_edit,name='wiki_edit'),
                url(r'^wiki/uoload/$',wiki.wiki_upload,name='wiki_upload'),

                url(r'^file/$',file.file,name='file'),
                url(r'^file_delete/$',file.file_delete,name='file_delete'),
                url(r'^file/post/$',file.file_post,name='file_post'),
                url(r'^file/download/(?P<file_id>\d+)$',file.download,name='file_download'),
                url(r'^cos/credential/$',file.cos_credential,name='cos_credential'),


                url(r'^setting/$',setting.setting,name='setting'),
                url(r'^setting/delete$',setting.delete,name='setting_delete'),

                url(r'^issues/$', issues.issues, name='issues'),
                url(r'^issues/detail/(?P<issues_id>\d+)/$', issues.issues_detail, name='issues_detail'),
                url(r'^issues/record/(?P<issues_id>\d+)/$', issues.issues_record, name='issues_record'),
                url(r'^issues/change/(?P<issues_id>\d+)/$', issues.issues_change, name='issues_change'),
                url(r'^issues/invite/url/$', issues.invite_url, name='invite_url'),

                url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
                url(r'^dashboard/issues/chart/$', dashboard.issues_chart, name='issues_chart'),
            ],None,None)),

            url(r'^invite/join/(?P<code>\w+)/$',issues.invite_join, name='invite_join'),
]