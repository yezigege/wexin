# -*- coding: utf-8 -*-
"""
功能: 上传图片生成二维码返回
github项目地址: https://github.com/sylnsfar/qrcode/blob/master/README-cn.md
"""
import json

import requests
import sys
import os
import logging
from MyQR import myqr

from cache import ctrl
from settings import KEY_ACCESS_TOKEN


IMAGES = os.path.join(sys.path[0], 'static/images/')  # 图片存储位置
QRCODE = os.path.join(sys.path[0], 'static/qrcodes/')  # 二维码存储位置


def download_img(url, name):

    logging.info("正在下载图片......")

    path = IMAGES + "{}.png".format(name)

    try:
        res = requests.get(url)
        img = res.content
        with open(path, 'wb') as f:
            f.write(img)
    except Exception as e:
        logging.debug("=======下载图片出错=======: {}".format(e))
        pass

    logging.info("=====图片下载完成=====")

    return path


def upload_img(mediatype, name):
    """
    因为个人公众号的原因，此函数可能并不能使用
    :param mediatype:
    :param name:
    :return:
    """
    logging.info("正在上传图片......")

    path = QRCODE + "{}.png".format(name)
    parse_json = {}
    try:
        token = ctrl.wx_rs.get_cache_ctl(KEY_ACCESS_TOKEN)
        url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" % (token, mediatype)
        files = {'media': open('{}'.format(path), 'rb')}
        r = requests.post(url, files=files)
        parse_json =json.loads(r.text)
        logging.info("上传图片数据返回值: {}".format(parse_json))
    except Exception as e:
        logging.error("图片上传错误信息记录===> {}".format(e))
    logging.info("====上传图片完成====")

    return parse_json['media_id'] if parse_json else []


def make_qrcode(url, name):

    print("正在制作二维码.......")

    my_qrcode = ''
    img_data = download_img(url, name)

    try:
        my_qrcode = myqr.run(
                # 原二维码扫描结果放下面引号中
                words=url,
                version=1,
                level='H',
                # 用于合成新二维码的动图
                picture=img_data,
                colorized=True,
                contrast=1.0,
                brightness=1.0,
                # 新二维码的文件名
                save_name="{}.png".format(name),
                # 新二维码的存储位置
                save_dir=QRCODE
            )

        print("二维码制作完成！")

    except Exception as e:
        logging.error(e)

    return my_qrcode
