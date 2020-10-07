
import django
import os
import sys
base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append((base_dir))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","blog_project")
django.setup()


from web import models
#往数据库添加数据，连接数据库，操作，关闭连接
models.UserInfo.objects.create(username='航',email='hanghang@live.com',mobile_phone='15667362250',password='123456789')