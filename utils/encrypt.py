#密码加密文件
import hashlib
from django.conf import settings
import uuid

def MD5(string):
    hash_object=hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_object.update(string.encode('utf-8'))
    return hash_object.hexdigest()

def uid(string):
    data = "{}-{}".format(str(uuid.uuid4()), string)
    return MD5(data)