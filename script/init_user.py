
import base

from web import models
#往数据库添加数据，连接数据库，操作，关闭连接
models.UserInfo.objects.create(username='航',email='hanghang@live.com',mobile_phone='15667362250',password='123456789')