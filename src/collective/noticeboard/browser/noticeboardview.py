#!/usr/bin/python
# -*- coding: utf-8 -*-

from Acquisition import aq_inner

# from Products.CMFPlone.utils import getToolByName

from Products.Five.browser import BrowserView
import json

from collective.noticeboard.interfaces import INote
from collective.noticeboard.settings import NoticeboardSettings

from plone.app.collection.interfaces import ICollection
from Products.ATContentTypes.interface import IATTopic
from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from zope.i18nmessageid import MessageFactory

PMF = MessageFactory('plone')


class NoticeboardView(BrowserView):

    def __call__(self):
        self.settings = NoticeboardSettings(self.context)
        return self.index()


class NoticeboardNotes(BrowserView):

    def __call__(self):
        self.request.response.setHeader('Content-Type',
                'application/json; charset=utf-8')

# if self.request.REQUEST_METHOD == 'POST': return self.handle_change()

        retval = []
        items = self.contents()
        check_perm = getSecurityManager().checkPermission
        for item in items:
            actions = []
            if check_perm(permissions.DeleteObjects, item):
                actions.append(dict(title=PMF('Delete'), class_='delete'
                               , url=item.absolute_url()
                               + '/delete_confirmation'))
            if check_perm(permissions.ModifyPortalContent, item):
                actions.append(dict(title=PMF('Edit'), class_='edit',
                               url=item.absolute_url() + '/edit'))
            note = INote(item)
            notedata = note.jsonable
            notedata.update(dict(actions=actions))
            retval.append(notedata)
        return json.dumps(retval)

    def contents(self):
        context = aq_inner(self.context)
        if IATTopic.providedBy(context):
            items = context.queryCatalog()
        elif ICollection.providedBy(context):
            items = self.context.results(batch=False, brains=False)
        else:
            items = context.getFolderContents(full_objects=True)
        return items
