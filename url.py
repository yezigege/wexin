# -*- coding: utf-8 -*-


from server.wxauthorize import WxSignatureHandler
from server.page_handler import PageHandler
from server.wx_handler import WxHandler


'''web解析规则'''

urlpatterns = [
    (r'/weixin', WxSignatureHandler),  # 微信签名
    (r'/page/(.*)', PageHandler),  # 加载页面
    (r'/wx/(.*)', WxHandler),  # 网页授权
]

# URLS = [
#     (r'tingyulin.cn',
#         (r'/(.*\.txt)', web.StaticFileHandler, {'path': STATIC_PATH}), # 微信域名检查用
#      )
#     ]
