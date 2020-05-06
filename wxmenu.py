# -*- coding: utf-8 -*-
import requests
import json
import logging

from cache import ctrl
from server.wxauthorize import WxAuthorServer
from settings import KEY_ACCESS_TOKEN, MENU_CREATE_URL, MENU_DELETE_URL, MENU_GET_URL


class WxMenuServer(object):
    """
    微信自定义菜单

    create_menu                     自定义菜单创建接口
    get_menu                        自定义菜单查询接口
    delete_menu                     自定义菜单删除接口
    create_menu_data                创建菜单数据
    """

    _wx_author_server = WxAuthorServer()  # 微信网页授权server

    def create_menu(self):
        """自定义菜单创建接口"""
        access_token = ctrl.wx_rs.get_cache_ctl(KEY_ACCESS_TOKEN)
        if access_token:
            url = MENU_CREATE_URL + access_token
            logging.info("url=====> {}".format(url))
            data = self.create_menu_data()
            r = requests.post(url, data.encode('utf-8'))
            logging.debug('【微信自定义菜单】自定义菜单创建接口Response[' + str(r.status_code) + ']')
            if r.status_code == 200:
                res = r.text
                logging.debug('【微信自定义菜单】自定义菜单创建接口' + res)
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            logging.info('【微信自定义菜单】自定义菜单创建接口获取不到access_token')

    def get_menu(self):
        """自定义菜单查询接口"""
        access_token = ctrl.wx_rs.get_cache_ctl(KEY_ACCESS_TOKEN)
        if access_token:
            url = MENU_GET_URL + access_token
            r = requests.get(url)
            logging.debug('【微信自定义菜单】自定义菜单查询接口Response[' + str(r.status_code) + ']')
            if r.status_code == 200:
                res = r.text
                logging.debug('【微信自定义菜单】自定义菜单查询接口' + res)
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            logging.info('【微信自定义菜单】自定义菜单查询接口获取不到access_token')

    def delete_menu(self):
        """自定义菜单删除接口"""
        access_token = ctrl.wx_rs.get_cache_ctl(KEY_ACCESS_TOKEN)
        if access_token:
            url = MENU_DELETE_URL + access_token
            r = requests.get(url)
            logging.debug('【微信自定义菜单】自定义菜单删除接口Response[' + str(r.status_code) + ']')
            if r.status_code == 200:
                res = r.text
                logging.debug('【微信自定义菜单】自定义菜单删除接口' + res)
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            logging.info('【微信自定义菜单】自定义菜单删除接口获取不到access_token')

    def create_menu_data(self):
        """创建菜单数据"""
        menu_data = {'button': []}  # 大菜单
        menu_Index0 = {
            'type': 'view',
            'name': '测试菜单1',
            'url': self._wx_author_server.get_code_url('menuIndex0')
        }
        menu_data['button'].append(menu_Index0)
        MENU_DATA = json.dumps(menu_data, ensure_ascii=False)
        logging.debug('【微信自定义菜单】创建菜单数据MENU_DATA[' + str(MENU_DATA) + ']')
        return MENU_DATA


if __name__ == '__main__':
    wx_menu_server = WxMenuServer()
    '''创建菜单数据'''
    # wx_menu_server.create_menu_data()
    # '''自定义菜单创建接口'''
    wx_menu_server.create_menu()
    '''自定义菜单查询接口'''
    # wx_menu_server.get_menu()
    '''自定义菜单删除接口'''
    # wx_menu_server.delete_menu()
