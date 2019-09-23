# -*- coding: utf-8 -*-
import logging
import tornado.ioloop
import requests
import json
from settings import CONFIG_GET_ACCESS_TOKEN_URL, KEY_ACCESS_TOKEN, KEY_JSAPI_TICKET, _EXPIRE_TIME_ACCESS_TOKEN
from cache import ctrl


class WxShedule(object):
    """
    定时任务调度器

    excute                      执行定时器任务
    get_access_token            获取微信全局唯一票据access_token
    get_jsapi_ticket           获取JS_SDK权限签名的jsapi_ticket
    """

    def excute(self):
        """执行定时器任务"""
        logging.info('【获取微信全局唯一票据access_token】>>>执行定时器任务')
        tornado.ioloop.IOLoop.instance().call_later(0, self.get_access_token)
        tornado.ioloop.PeriodicCallback(self.get_access_token, _EXPIRE_TIME_ACCESS_TOKEN).start()
        # tornado.ioloop.IOLoop.current().start()

    def get_access_token(self):
        """获取微信全局唯一票据access_token"""
        res = requests.get(CONFIG_GET_ACCESS_TOKEN_URL)
        data = eval(res.content.decode())
        ctrl.wx_rs.set_access_cache_ctl(
            KEY_ACCESS_TOKEN,
            data["access_token"],
        )

    def get_jsapi_ticket(self):
        """获取JS_SDK权限签名的jsapi_ticket"""
        access_token = ctrl.wx_rs.get_cache_ctl(KEY_ACCESS_TOKEN)
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
                    ctrl.wx_rs.set_access_cache_ctl(KEY_JSAPI_TICKET, jsapi_ticket)
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
