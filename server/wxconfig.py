# -*- coding: utf-8 -*-
class WxConfig(object):
    """
    微信开发--基础配置

    """
    AppID = 'wx2fb730103c560374'  # AppID(应用ID)
    AppSecret = '78cc90b8ee614b06b97abeb8dcf6d668'  # AppSecret(应用密钥)

    '''获取access_token'''
    config_get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_' \
                                  'type=client_credential&appid=%s&secret=%s' % (AppID, AppSecret)
