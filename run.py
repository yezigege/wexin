# -*- coding: utf-8 -*-


import os
import sys
import base64
import uuid
from tornado import web, ioloop, httpserver
from tornado.options import define, options
from url import urlpatterns
from wxshedule import WxShedule

define('port', default=80, help='run on the given port', type=int)
define('debug', default=True, help='enable debug mode')


STATIC_PATH = os.path.join(sys.path[0], 'static')
TPL_PATH = os.path.join(sys.path[0], 'template')


class Application(web.Application):
    def __init__(self):
        settings = dict(
            template_path=TPL_PATH,
            static_path=STATIC_PATH,
            debug=True,
            login_url='/login',
            cookie_secret=base64.b64encode(uuid.uuid3(uuid.NAMESPACE_DNS, 'wechat').bytes),
        )
        super(Application, self).__init__(urlpatterns, **settings)


def main():
    options.parse_command_line()  # 转换命令行参数，使得启动时命令行参数可以应用到项目中
    application = Application()
    http_server = httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)

    # 执行定时任务
    wx_shedule = WxShedule()
    wx_shedule.excute()
    loop = ioloop.IOLoop.instance()
    loop.start()


if __name__ == '__main__':
    main()
