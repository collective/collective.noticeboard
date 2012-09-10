#!/usr/bin/python
# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
import json

from collective.noticeboard.settings import NoticeboardSettings
from collective.noticeboard.interfaces import INote, INoteMarker


class NoticeboardView(BrowserView):

    def __call__(self):
        self.settings = NoticeboardSettings(self.context)
        return self.index()


class NoticeboardNotes(BrowserView):

    def __call__(self):
        self.request.response.setHeader('Content-Type',
                'application/json; charset=utf-8')
        retval = []
        for item in self.context.objectValues():
            if INoteMarker.providedBy(item):
                note = INote(item)
                retval.append(dict(text=note.text,
                              image_url=note.image_url,
                              position_x=note.position_x,
                              position_y=note.position_y))
        return json.dumps(retval)
