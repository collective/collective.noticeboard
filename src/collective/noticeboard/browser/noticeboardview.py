#!/usr/bin/python
# -*- coding: utf-8 -*-

from Acquisition import aq_inner
# from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView
import json

from collective.noticeboard.interfaces import INote, INoteMarker
from collective.noticeboard.settings import NoticeboardSettings

from plone.app.collection.interfaces import ICollection
from Products.ATContentTypes.interface import IATTopic
# from plone.app.contentlisting.interfaces import IContentListing
# from zope.component.hooks import getSite


class NoticeboardView(BrowserView):

    def __call__(self):
        self.settings = NoticeboardSettings(self.context)
        return self.index()


class NoticeboardNotes(BrowserView):

    def __call__(self):
        self.request.response.setHeader('Content-Type',
                'application/json; charset=utf-8')
        if self.request.REQUEST_METHOD == 'POST':
            return self.handle_change()
        retval = []
        items = self.contents()
        for item in items:
#            if INoteMarker.providedBy(item):
            note = INote(item)
            retval.append(dict(
                        title=note.title,
                        descripton=note.description,
                        text=note.text,
                        image_url=note.image_url,
                        position_x=note.position_x,
                        position_y=note.position_y))
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
