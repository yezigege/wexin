# -*- coding: utf-8 -*-
import logging
from settings import _EXPIRE_ACCESS_TOKEN, _EXPIRE_JS_TOKEN


class WexinCtrl(object):
    """
    微信token缓存

    set_cache               添加redis
    get_cache               获取redis
    """
    def __init__(self, ctrl):
        self.ctrl = ctrl

    def set_access_cache(self, key, value):
        """添加微信access_token验证相关redis"""
        res = self.ctrl.rs.set(key, value, ex=_EXPIRE_ACCESS_TOKEN)
        logging.error('【微信token缓存】setCache>>>key[' + key + '],value[' + value + ']')
        return res

    def set_js_cache(self, key, value):
        """添加网页授权相关redis"""
        res = self.ctrl.rs.set(key, value, ex=_EXPIRE_JS_TOKEN)
        logging.error('【微信token缓存】setCache>>>key[' + key + '],value[' + value + ']')
        return res

    def get_cache(self, key):
        """获取redis"""
        try:
            v = (self.ctrl.rs.get(key)).decode('utf-8')
            logging.error(v)
            logging.error('【微信token缓存】getCache>>>key[' + key + '],value[' + v + ']')
            return v
        except Exception as e:
            logging.error(e)
            return None
