# -*- coding: utf-8 -*-
import logging
import tornado.ioloop
import requests
import json
from server.wxconfig import WxConfig
from cache.tokencache import TokenCache


class WxShedule(object):
    """
    定时任务调度器

    excute                      执行定时器任务
    get_access_token            获取微信全局唯一票据access_token
    get_jsapi_ticket           获取JS_SDK权限签名的jsapi_ticket
    """
    _token_cache = TokenCache()  # 微信token缓存实例
    _expire_time_access_token = 7000 * 1000  # token过期时间

    def excute(self):
        """执行定时器任务"""
        logging.info('【获取微信全局唯一票据access_token】>>>执行定时器任务')
        tornado.ioloop.IOLoop.instance().call_later(0, self.get_access_token)
        tornado.ioloop.PeriodicCallback(self.get_access_token, self._expire_time_access_token).start()
        # tornado.ioloop.IOLoop.current().start()

    def get_access_token(self):
        """获取微信全局唯一票据access_token"""
        res = requests.get(WxConfig.config_get_access_token_url)
        data = eval(res.content.decode())
        logging.error("res: {}".format(res.content))
        self._token_cache.set_access_cache(
            self._token_cache.KEY_ACCESS_TOKEN,
            data["access_token"],
        )

    def get_jsapi_ticket(self):
        """获取JS_SDK权限签名的jsapi_ticket"""
        access_token = self._token_cache.get_cache(self._token_cache.KEY_ACCESS_TOKEN)
        if access_token:
            url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % access_token
            r = requests.get(url)
            logging.info('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket的Response[' + str(r.status_code) + ']')
            if r.status_code == 200:
                res = r.text
                logging.info('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket>>>>' + res)
                d = json.loads(res)
                errcode = d['errcode']
                if errcode == 0:
                    jsapi_ticket = d['ticket']
                    # 添加至redis中
                    self._token_cache.set_access_cache(self._token_cache.KEY_JSAPI_TICKET, jsapi_ticket)
                else:
                    logging.info('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket>>>>errcode[' + errcode + ']')
                    logging.info('【微信JS-SDK】request jsapi_ticket error, will retry get_jsapi_ticket() method after 10s')
                    tornado.ioloop.IOLoop.instance().call_later(10, self.get_jsapi_ticket)
            else:
                logging.info('【微信JS-SDK】request jsapi_ticket error, will retry get_jsapi_ticket() method after 10s')
                tornado.ioloop.IOLoop.instance().call_later(10, self.get_jsapi_ticket)
        else:
            logging.error(
                '【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket时,access_token获取失败, will retry get_access_token() method after 10s')
            tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)


if __name__ == '__main__':
    wx_shedule = WxShedule()
    """执行定时器"""
    wx_shedule.excute()
