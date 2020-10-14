
from django.conf.urls import url
from web.views import account
from web.views import home
from web.views import project_list
from django.conf.urls import include
from web.views import manage
from web.views import wiki
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
    url(r'^manage/(?P<project_id>\d+)/',include([
            url(r'^dashboard/$',manage.dashboard,name='dashboard'),
            url(r'^issues/$',manage.issues,name='issues'),
            url(r'^statistic/$',manage.statistic,name='statistic'),
            url(r'^file/$',manage.file,name='file'),
            url(r'^wiki/$',wiki.wiki,name='wiki'),
            url(r'^wiki/add/$',wiki.wiki_add,name='wiki_add'),
            url(r'^wiki/catalog/$',wiki.wiki_catalog,name='wiki_catalog'),
            url(r'^wiki/delete/(?P<wiki_id>\d+)$',wiki.wiki_delete,name='wiki_delete'),
            url(r'^wiki/edit/(?P<wiki_id>\d+)$',wiki.wiki_edit,name='wiki_edit'),
            url(r'^wiki/uoload/$',wiki.wiki_upload,name='wiki_upload'),
            # url(r'^wiki/detail/$',wiki.wiki_detail,name='wiki_detail'),
            url(r'^setting/$',manage.setting,name='setting'),
        ],None,None)),
]