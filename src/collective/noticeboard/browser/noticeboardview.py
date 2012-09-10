#!/usr/bin/python
# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
import json

from collective.noticeboard.settings import NoticeboardSettings


class NoticeboardView(BrowserView):

    def __call__(self):
        self.settings = NoticeboardSettings(self.context)
        return self.index()


class NoticeboardNotes(BrowserView):
    def __call__(self):
        self.request.response.setHeader("Content-Type",
            "application/json; charset=utf-8")
        return json.dumps([{}])
