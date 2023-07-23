'''
Author: Misaki
Date: 2023-07-19 14:42:17
LastEditTime: 2023-07-19 14:42:21
LastEditors: Misaki
Description: 
'''

LANGUAGE_CODE = 'zh-hans'

# django
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.3.86:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "foobared" # redis密码
        }
    }
}

# 短信服务
ALI_ACCESS = {
    'ACCESS_KEY_ID': '',
    'ACCESS_KEY_SECRET': ''
}
