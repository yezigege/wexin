from wxauthorize import WxSignatureHandler
from tornado import web

'''web解析规则'''

urlpatterns = [
    (r'/weixin', WxSignatureHandler),  # 微信签名
]

# URLS = [
#     (r'tingyulin.cn',
#         (r'/(.*\.txt)', web.StaticFileHandler, {'path': STATIC_PATH}), # 微信域名检查用
#      )
#     ]
