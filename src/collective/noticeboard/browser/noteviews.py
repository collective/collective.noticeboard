#!/usr/bin/python
# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
import json

from collective.noticeboard.interfaces import INote


class NoticePUTView(BrowserView):

    def __call__(self):
        pos = self.request.stdin.tell()
        self.request.stdin.seek(0)
        try:
            data = json.loads(self.request.stdin.read())
        finally:
            self.request.stdin.seek(pos)
        note = INote(self.context)
        note.position_x = data['position_x']
        note.position_y = data['position_y']
