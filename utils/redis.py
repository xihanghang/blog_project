from django_redis import get_redis_connection
from django.shortcuts import HttpResponse

def index(request):
    #去连接池获取一个连接
    conn=get_redis_connection("default")
    conn.set('15667362251',1234,ex=60)
    value=conn.get('15667362251')
    print(value)
    return HttpResponse('ok')
