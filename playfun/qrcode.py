# -*- coding: utf-8 -*-
"""
功能: 上传图片生成二维码返回
github项目地址: https://github.com/sylnsfar/qrcode/blob/master/README-cn.md
"""
import requests
import sys
import os
import logging
from MyQR import myqr


IMAGES = os.path.join(sys.path[0], 'static/images')  # 图片存储位置


def download_img(url, name):

    logging.info("正在下载图片......")

    path = IMAGES + "{}.png".format(name)

    try:
        res = requests.get(url)
        img = res.content
        logging.error("图片存储名称及位置: {}".format(path))
        with open(path, 'wb') as f:
            f.write(img)
    except Exception as e:
        logging.error("=======下载图片出错=======: {}".format(e))
        pass

    logging.info("=====图片下载完成=====")

    return path


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
                save_dir=sys.path[0]
            )

        print("二维码制作完成！")

    except Exception as e:
        logging.error(e)

    return my_qrcode
