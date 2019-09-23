#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cache.basecache import rs
from cache.wx_rs import WexinCtrl


class Ctrl(object):

    def __init__(self):
        self.__method_ren()

        self.rs = rs

        self.wx_rs = WexinCtrl(self)

    def __method_ren(self):
        """
        重命名control下的函数名，防止命名冲突
        """
        for std in globals():
            if std.find('Ctrl') == -1:
                continue

            cls = globals()[std]
            for func in dir(cls):
                if callable(getattr(cls, func)) and not func.startswith('__'):
                    setattr(cls, '%s_ctl' % func, getattr(cls, func))
                    delattr(cls, func)


# global, called by handler
ctrl = Ctrl()

