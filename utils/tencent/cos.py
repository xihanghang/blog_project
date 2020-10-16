# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
def create_bucket(bucket,region='ap-chengdu'):
    # token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
    # scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    # # 2. 获取客户端对象
    client = CosS3Client(config)
    # 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py
    client.create_bucket(
        Bucket=bucket,
        ACL="public-read",  #privatepublic-read-write
    )

def upload_file(bucket,region,file_object,key):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    # # 2. 获取客户端对象
    client = CosS3Client(config)
    # 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

    response = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=file_object,
        Key=key
    )
    print(response['ETag'])
    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket,region,key)

def delete_file(bucket,region,key):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    # # 2. 获取客户端对象
    client = CosS3Client(config)
    # 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py

    client.delete_object(
        Bucket=bucket,
        Key=key
    )

def delete_file_list(bucket,region,key_list):
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    # # 2. 获取客户端对象
    client = CosS3Client(config)
    # 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py
    objects = {
        "Quiet": "true",
        "Object": key_list
    }
    client.delete_objects(
        Bucket=bucket,
        Delete=objects
    )
