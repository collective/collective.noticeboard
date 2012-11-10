#!/usr/bin/python
# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
import json

from collective.noticeboard.interfaces import INote
from collective.noticeboard.settings import NoticeboardSettings

from plone.app.collection.interfaces import ICollection
from Products.ATContentTypes.interface import IATTopic
from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from datetime import datetime, timedelta
from collective.noticeboard import _
from Products.CMFPlone import PloneMessageFactory as PMF


class NoticeboardView(BrowserView):

    def __call__(self):
        self.settings = NoticeboardSettings(self.context)
        return self.index()

    def note_type(self):
        return self.settings.note_type.replace(' ', '+')


class NoticeboardNotes(BrowserView):

    def __call__(self):
        self.request.response.setHeader('Content-Type',
                                        'application/json; charset=utf-8')
        retval = []
        new = []
        max_zindex = 0
        items = self.contents()
        check_perm = getSecurityManager().checkPermission
        delete_url = None
        settings = NoticeboardSettings(self.context)
        hide_after = settings.hide_after_days
        limit = datetime.now() - timedelta(days=hide_after)
        for item in items:
            if hide_after:
                # ignore items that are older than the limit
                created = item.created().utcdatetime()
                if created <= limit:
                    continue
            actions = []
            note = INote(item)
            if check_perm(permissions.ModifyPortalContent, item):
                if note.review_state == 'private':
                    actions.append(dict(content=PMF('Publish'),
                                        title="",
                                        class_='publish',
                                        url=item.absolute_url() +
                            '/content_status_modify?workflow_action=publish'))
        # alternatively use a popup with the form from /content_status_history

                actions.append(dict(content='Color',
                                    title=_("Change color"),
                                    class_='change_color',
                                    url=item.absolute_url() + '/change_color'))
                actions.append(dict(content=PMF('Edit'),
                                    title='',
                                    class_='edit',
                                    url=item.absolute_url() + '/edit'))

            if check_perm(permissions.DeleteObjects, item):
                delete_url = item.absolute_url() \
                    + '/delete_confirmation'
                actions.append(dict(content=PMF('Delete'),
                                    title='',
                                    class_='delete',
                                    url=delete_url))
            notedata = note.jsonable
            try:
                max_zindex = max(max_zindex, int(note.zIndex))
            except ValueError:
                new.append(notedata)
            notedata.update(dict(hasactions=bool(actions)))
            notedata.update(dict(actions=actions))

            if delete_url:
                notedata.update(dict(delete_url=delete_url))
            retval.append(notedata)
        for (new_note, new_index) in zip(new, range(max_zindex + 1,
                                         max_zindex + len(new) + 1)):
            new_note['zIndex'] = new_index
        return json.dumps(retval)

    def contents(self):
        """ Get the contents of the folder/collection.
        """

        context = aq_inner(self.context)
        if IATTopic.providedBy(context):
            items = context.queryCatalog()
        elif ICollection.providedBy(context):
            items = self.context.results(batch=False, brains=False)
        else:
            items = context.getFolderContents(full_objects=True)
        return items
