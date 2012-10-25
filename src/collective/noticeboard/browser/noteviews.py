#!/usr/bin/python
# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
import json
from logging import getLogger

from collective.noticeboard.interfaces import INote

logging = getLogger(__name__)


class NoticeJSONView(BrowserView):

    def __call__(self):
        actions = dict(PUT=self.put, GET=self.get)
        note = INote(self.context)
        return json.dumps(actions[self.request.getHeader('HTTP_X_HTTP_METHOD_OVERRIDE', "GET"
                          )](note))

    def get(self, note):
        logging.info('Object retrieved %s' % str(note.jsonable))
        return note.jsonable

    def put(self, note):
        pos = self.request.stdin.tell()
        self.request.stdin.seek(0)
        try:
            data = json.loads(self.request.stdin.read())
        finally:
            self.request.stdin.seek(pos)
        note = INote(self.context)
        note.position_x = data['position_x']
        note.position_y = data['position_y']
        note.height = data['height']
        note.width = data['width']
        note.color = data['color']
        note.zIndex = data['zIndex']
        logging.info('Object updated %s' % str(data))
        return True
