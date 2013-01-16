#!/usr/bin/python
# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from Acquisition import aq_parent
from logging import getLogger
from Products.CMFCore import permissions
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
import json

from collective.noticeboard import _
from collective.noticeboard.interfaces import INote

logging = getLogger(__name__)


class NoticeJSONView(BrowserView):

    def __call__(self):
        actions = dict(PUT=self.put, GET=self.get, DELETE=self.delete)
        note = INote(self.context)
        key = self.request.getHeader('HTTP_X_HTTP_METHOD_OVERRIDE',
                                     'GET')
        return json.dumps(actions[key](note))

    def _check_permission(self, perm):
        sm = getSecurityManager()
        if not sm.checkPermission(perm, self.context):
            portal_state = getMultiAdapter(
                (self.context, self.request), name=u'plone_portal_state')
            member = portal_state.member()
            logging.error(
                'Failed permission check. Required Permission "%s", user "%s"',
                perm, member)
            raise Unauthorized(_('You do not have the required permission'))
        return True

    def get(self, note):
        logging.debug('Object retrieved %s' % str(note.jsonable))
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
        logging.debug('Object updated %s' % str(data))
        return True

    def delete(self, note):
        self._check_permission(permissions.DeleteObjects)
        aq_parent(self.context).manage_delObjects(self.context.id)
        return True
