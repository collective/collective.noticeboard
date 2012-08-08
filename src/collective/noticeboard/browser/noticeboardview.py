#!/usr/bin/python
# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView

from collective.noticeboard.settings import NoticeboardSettings


class NoticeboardView(BrowserView):

    def __call__(self):
        self.settings = NoticeboardSettings(self.context)
        return self.index()
