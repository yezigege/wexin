# -*- coding: utf-8 -*-
"""
微信开发--基础配置

"""
APPID = 'wx2fb730103c560374'  # AppID(应用ID)
APPSECRET = '78cc90b8ee614b06b97abeb8dcf6d668'  # AppSecret(应用密钥)


"""redis 配置"""
REDIS = {
    'host': '127.0.0.1',
    'port': 6379,
    'database': 0,
}

"""关注回复消息"""
SUBSCRIBE_CONTENT = "地球人，你好！"

'''获取access_token'''
CONFIG_GET_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_' \
                              'type=client_credential&appid=%s&secret=%s' % (APPID, APPSECRET)

"""微信网页开发域名"""
APPHOST = 'http://www.tingyulin.cn'

'''微信公众号菜单映射数据'''
"""重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节"""
WX_MENU_STATE_MAP = {
    'menuIndex0': '%s/page/index' % APPHOST,  # 测试菜单1
}

# 自定义菜单
# 删除接口
MENU_DELETE_URL = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
# 查询接口
MENU_GET_URL = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token="
# 创建接口
MENU_CREATE_URL = " https://api.weixin.qq.com/cgi-bin/menu/create?access_token="


_EXPIRE_ACCESS_TOKEN = 7200  # 微信access_token过期时间, 2小时
_EXPIRE_JS_TOKEN = 30 * 24 * 3600  # 微信js网页授权过期时间, 30天
KEY_ACCESS_TOKEN = 'access_token'  # 微信全局唯一票据access_token
KEY_JSAPI_TICKET = 'jsapi_ticket'  # JS_SDK权限签名的jsapi_ticket

_EXPIRE_TIME_ACCESS_TOKEN = 7000 * 1000  # token过期时间

