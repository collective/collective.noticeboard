#!/usr/bin/python
# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Acquisition import aq_inner
from collective.noticeboard.interfaces import INote
from collective.noticeboard.settings import NoticeboardSettings
from datetime import datetime, timedelta
from plone.app.collection.interfaces import ICollection
from Products.ATContentTypes.interface import IATTopic
from Products.CMFCore import permissions
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
import json

from collective.noticeboard import _

class NoticeboardView(BrowserView):
    """ The canvas that contains the notes
    """

    def __call__(self):
        self.settings = NoticeboardSettings(self.context)
        return self.index()

    def note_type(self):
        return self.settings.note_type.replace(' ', '+')

    def can_add(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        if portal_state.anonymous():
            # we want to show the login-form
            return True
        check_perm = getSecurityManager().checkPermission
        return check_perm(permissions.AddPortalContent, self.context)

    def can_edit(self):
        check_perm = getSecurityManager().checkPermission
        return check_perm(permissions.ModifyPortalContent, self.context)

    def images_visible(self):
        if "Image" in self.settings.display_types or self.settings.note_type == "Image":
            return True
        return False

    def showhelp(self):
        return self.settings.showhelp

class NoticeboardNotes(BrowserView):
    """ The json-dump of notes
    """

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
            if item.exclude_from_nav():
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
        settings = NoticeboardSettings(self.context)
        display_types = settings.display_types
        display_types.append(settings.note_type)
        display_types = list(set(display_types))
        if IATTopic.providedBy(context):
            # handle old collections
            items = context.queryCatalog(portal_types=display_types)
        elif ICollection.providedBy(context):
            # handle new collections
            items = self.context.results(batch=False, brains=False)
        else:
            # handle folders
            items = context.getFolderContents(full_objects=True,
                        contentFilter={"portal_type":display_types,
                                       "sort_on":"created"})
        return items


class NoticeboardArchive(NoticeboardNotes):
    """ A listing-view of all outdated items
    """

    def __call__(self):
        """ Render the content item listing.
        """

        notes = []
        items = self.contents()
        settings = NoticeboardSettings(self.context)
        hide_after = settings.hide_after_days
        limit = datetime.now() - timedelta(days=hide_after)
        for item in items:
            if hide_after:
                # ignore items that are newer than the limit
                created = item.created().utcdatetime()
                if created >= limit:
                    continue
            notes.append(item)
        self.contents = notes
        return self.index()

