# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from django.conf import settings
from qcloud_cos.cos_exception import CosServiceError

from django.http import JsonResponse
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

    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': "*",
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader':"*",
                'ExposeHeader':"*",
                'MaxAgeSeconds': 500
            }
        ]
    }
    client.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration=cors_config
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

def credential(bucket,region):

    from sts.sts import Sts

    config = {
        #临时密钥有效时长，单位为秒
        'duration_seconds': 1800,
        # 固定密钥 id
        'secret_id': settings.TENCENT_SECRET_ID,
        # 固定密钥 key
        'secret_key': settings.TENCENT_SECRET_KEY,
        # 换成你的 bucket
        'bucket': bucket,
        # 换成 bucket 所在地区
        'region': region,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            # "name/cos:PutObject",
            # 'name/cos:PostObject',
            # 'name/cos:DeleteObject',
            # "name/cos:UploadPart",
            # "name/cos:UploadPartCopy",
            # "name/cos:CompleteMultipartUpload",
            # "name/cos:AbortMultipartUpload",
            "*",
        ],

    }

    sts = Sts(config)
    result_dict = sts.get_credential()
    return result_dict

def delete_bucket(bucket, region):
    """ 删除桶 """
    # 删除桶中所有文件
    # 删除桶中所有碎片
    # 删除桶
    config = CosConfig(Region=region, SecretId=settings.TENCENT_SECRET_ID, SecretKey=settings.TENCENT_SECRET_KEY)
    client = CosS3Client(config)

    try:
        # 找到文件 & 删除
        while True:
            part_objects = client.list_objects(bucket)

            # 已经删除完毕，获取不到值
            contents = part_objects.get('Contents')
            if not contents:
                break

            # 批量删除
            objects = {
                "Quiet": "true",
                "Object": [{'Key': item["Key"]} for item in contents]
            }
            client.delete_objects(bucket, objects)

            if part_objects['IsTruncated'] == "false":
                break

        # 找到碎片 & 删除
        while True:
            part_uploads = client.list_multipart_uploads(bucket)
            uploads = part_uploads.get('Upload')
            if not uploads:
                break
            for item in uploads:
                client.abort_multipart_upload(bucket, item['Key'], item['UploadId'])
            if part_uploads['IsTruncated'] == "false":
                break

        client.delete_bucket(bucket)
    except CosServiceError as e:
        pass

