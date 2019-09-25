# -*- coding: utf-8 -*-
import time
import json
from urllib import parse
import requests
import hashlib
import tornado.web
import xml.etree.ElementTree as ET
import logging

from playfun.qrcode import make_qrcode, upload_img
from cache import ctrl
from settings import APPHOST, APPID, APPSECRET, SUBSCRIBE_CONTENT


class WxSignatureHandler(tornado.web.RequestHandler):
    """
    微信服务器签名验证, 消息回复

    check_signature: 校验signature是否正确
    """
    def data_received(self, chunk):
        pass

    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            logging.debug(
                '微信sign校验,signature=' + signature + ',&timestamp=' + timestamp + '&nonce=' + nonce + '&echostr=' + echostr)
            result = self.check_signature(signature, timestamp, nonce)
            if result:
                logging.debug('微信sign校验,返回echostr=' + echostr)
                self.write(echostr)
            else:
                logging.error('微信sign校验,---校验失败')
        except Exception as e:
            logging.error('微信sign校验,---Exception' + str(e))

    def check_signature(self, signature, timestamp, nonce):
        """校验token是否正确"""
        token = 'dzyxwyk9390'
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        logging.debug('sha1=' + sha1 + '&signature=' + signature)
        return sha1 == signature

    def post(self):
        body = self.request.body
        logging.error('微信消息回复中心】收到用户消息 \n' + str(body.decode()))
        data = ET.fromstring(body)
        ToUserName = data.find('ToUserName').text
        FromUserName = data.find('FromUserName').text
        MsgType = data.find('MsgType').text
        Content = reply_content = reply_img = ''
        num = ctrl.rs.incr('qrs_show_num_%s' % FromUserName)
        if MsgType == 'text' or MsgType == 'voice' or MsgType == 'image':
            logging.info("收到消息......")
            '''文本消息 or 语音消息 or 图片消息'''
            try:
                MsgId = data.find("MsgId").text
                if MsgType == 'text':
                    Content = data.find('Content').text  # 文本消息内容
                elif MsgType == 'voice':
                    Content = data.find('Recognition').text  # 语音识别结果，UTF8编码
                elif MsgType == 'image':
                    MediaId = data.find('MediaId').text
                    img_url = data.find('PicUrl').text  # 图片消息内容(图片地址)
                    qr_name = FromUserName + '_' + str(num)
                    img_data = make_qrcode(img_url, qr_name)

                    if img_data:
                        try:
                            res = upload_img(MsgType, qr_name)
                        except:
                            logging.error("#######上传图片失败########")
                            pass

                        reply_img = res
                        logging.error("====={}=====".format(reply_img))
            except Exception as e:
                logging.error(e)
                pass

        if reply_img:
            print("调用发图片消息模板")
            CreateTime = int(time.time())
            out = self.reply_image(self, FromUserName, ToUserName, CreateTime, MsgType, reply_img)
            self.write(out)
            logging.info("________图片消息回复成功_______")
            return

        if Content == u'你好':
            reply_content = '您好,请问有什么可以帮助您的吗?'
        else:
            # 查找不到关键字,默认回复
            reply_content = "小叶子正在慢悠悠的开发中~"

        if reply_content:
            CreateTime = int(time.time())
            out = self.reply_text(self, FromUserName, ToUserName, CreateTime, MsgType, reply_content)
            self.write(out)
            logging.info("________消息回复成功_______")

        elif MsgType == 'event':
            '''接收事件推送'''
            try:
                Event = data.find('Event').text
                if Event == 'subscribe':
                    # 关注事件
                    CreateTime = int(time.time())
                    reply_content = SUBSCRIBE_CONTENT
                    out = self.reply_text(self, FromUserName, ToUserName, CreateTime, 'text', reply_content)
                    self.write(out)
            except:
                pass

    @staticmethod
    def reply_text(self, FromUserName, ToUserName, CreateTime, MsgType, Content):
        """回复文本消息模板"""
        textTpl = """<xml> 
                         <ToUserName><![CDATA[%s]]></ToUserName> 
                         <FromUserName><![CDATA[%s]]></FromUserName> 
                         <CreateTime>%s</CreateTime> 
                         <MsgType><![CDATA[%s]]></MsgType> 
                         <Content><![CDATA[%s]]></Content>
                     </xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, MsgType, Content)
        return out

    @staticmethod
    def reply_image(self, FromUserName, ToUserName, CreateTime, MsgType, MediaId):
        """回复图片消息模板"""
        imgTpl = """<xml> 
                         <ToUserName><![CDATA[%s]]></ToUserName> 
                         <FromUserName><![CDATA[%s]]></FromUserName> 
                         <CreateTime>%s</CreateTime> 
                         <MsgType><![CDATA[%s]]></MsgType> 
                         <Image><MediaId><![CDATA[%s]]></MediaId></Image>
                     </xml>"""
        out = imgTpl % (FromUserName, ToUserName, CreateTime, MsgType, MediaId)
        logging.error('微信消息回复中心回复用户消息 \n' + out)

        return out


class WxAuthorServer(object):
    """
    微信网页授权server

    get_code_url                            获取code的url
    get_auth_access_token                   通过code换取网页授权access_token
    refresh_token                           刷新access_token
    get_userinfo                            拉取用户信息
    """

    """授权后重定向的回调链接地址，请使用urlencode对链接进行处理"""
    REDIRECT_URI = '%s/wx/wxauthor' % APPHOST

    """
    应用授权作用域
    snsapi_base （不弹出授权页面，直接跳转，只能获取用户openid）
    snsapi_userinfo （弹出授权页面，可通过openid拿到昵称、性别、所在地。并且，即使在未关注的情况下，只要用户授权，也能获取其信息）
    """
    SCOPE = 'snsapi_base'
    # SCOPE = 'snsapi_userinfo'

    """通过code换取网页授权access_token"""
    get_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?'

    """拉取用户信息"""
    get_userinfo_url = 'https://api.weixin.qq.com/sns/userinfo?'

    def get_code_url(self, state):
        """获取code的url"""
        dict = {'redirect_uri': self.REDIRECT_URI}
        redirect_uri = parse.urlencode(dict)
        author_get_code_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&%s&response_type=code&scope=%s&state=%s#wechat_redirect' % (APPID, redirect_uri, self.SCOPE, state)
        logging.debug('【微信网页授权】获取网页授权的code的url>>>>' + author_get_code_url)
        return author_get_code_url

    def get_auth_access_token(self, code):
        """通过code换取网页授权access_token"""
        url = self.get_access_token_url + 'appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (APPID, APPSECRET, code)
        r = requests.get(url)
        logging.debug('【微信网页授权】通过code换取网页授权access_token的Response[' + str(r.status_code) + ']')
        if r.status_code == 200:
            res = r.text
            logging.debug('【微信网页授权】通过code换取网页授权access_token>>>>' + res)
            json_res = json.loads(res)
            if 'access_token' in json_res.keys():
                return json_res
            elif 'errcode' in json_res.keys():
                errcode = json_res['errcode']

    def get_userinfo(self, access_token, openid):
        """拉取用户信息"""
        url = self.get_userinfo_url + 'access_token=%s&openid=%s&lang=zh_CN' % (access_token, openid)
        r = requests.get(url)
        logging.debug('【微信网页授权】拉取用户信息Response[' + str(r.status_code) + ']')
        if r.status_code == 200:
            res = r.text
            json_data = json.loads((res.encode('iso-8859-1')).decode('utf-8'))
            logging.debug('【微信网页授权】拉取用户信息>>>>' + str(json_data))
