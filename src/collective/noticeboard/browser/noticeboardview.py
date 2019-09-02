# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.Five.browser import BrowserView
from collective.noticeboard import _
from collective.noticeboard import permissions as own_permissions
from collective.noticeboard.interfaces import INote
from collective.noticeboard.settings import NoticeboardSettings
from datetime import datetime, timedelta
from plone.app.contentlisting.catalog import CatalogContentListingObject
from zope.component import getMultiAdapter
from plone.app.contenttypes.interfaces import ICollection

import json
from six.moves import range
from six.moves import zip

try:
    from plone.app.collection.interfaces import ICollection as IATCollection
    HAS_AT_COLLECTIONS = True
except ImportError:
    HAS_AT_COLLECTIONS = False

try:
    from Products.ATContentTypes.interface import IATTopic
    HAS_AT_TOPIC = True
except ImportError:
    HAS_AT_TOPIC = False


class NoticeboardView(BrowserView):
    """ The canvas that contains the notes and the UI
    """

    def __call__(self):
        self.settings = NoticeboardSettings(self.context)
        return self.index()

    def note_type(self):
        return self.settings.note_type

    def show_login_as_add_link(self):
        if self.show_add_link():
            return False
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        return portal_state.anonymous()

    def show_add_link(self):
        check_perm = getSecurityManager().checkPermission
        return check_perm(permissions.AddPortalContent, self.context)

    def has_add_permission(self):
        check_perm = getSecurityManager().checkPermission
        return check_perm(permissions.AddPortalContent, self.context)

    def can_edit(self):
        check_perm = getSecurityManager().checkPermission
        return check_perm(own_permissions.manage_noticeboard, self.context)

    def images_visible(self):
        if "Image" in self.settings.display_types or self.settings.note_type == "Image":  # noqa
            return True
        return False

    def show_help(self):
        return self.settings.show_help

    def show_archive(self):
        return self.settings.hide_after_days

    def add_url(self):
        if self.context.portal_type in ["Collection", "Topic"]:
            container = self.context.__parent__
        else:
            container = self.context
        return container.absolute_url()

    def add_method(self, type_name):
        pt = getToolByName(self.context, 'portal_types')
        type_info = pt.getTypeInfo(self.settings.note_type)
        if type_info.content_meta_type.startswith("Dexterity"):
            return "++add++%s" % type_name.replace(' ', '%20')
        else:
            return "createObject?type_name=%s&ajax_load=1&ajax_include_head=1".format(type_name.replace(' ', '+'))  # noqa: E501


class NoticeboardNotes(BrowserView):
    """ The json-dump of notes
    """

    def __call__(self):  # noqa
        self.request.response.setHeader('Content-Type',
                                        'application/json; charset=utf-8')
        self.request.response.setHeader('Expires', '-1')
        self.request.response.setHeader('Cache-Control', 'private')
        retval = []
        new = []
        max_zindex = 0
        items = self.contents()
        check_perm = getSecurityManager().checkPermission
        delete_url = None
        settings = NoticeboardSettings(self.context)
        hide_after = settings.hide_after_days
        if hide_after:
            limit = datetime.now() - timedelta(days=hide_after)
        for item in items:
            if isinstance(item, CatalogContentListingObject):
                item = item.getObject()
            item = aq_inner(item)
            if hide_after:
                # ignore items that are older than the limit
                modified = item.modified().utcdatetime()
                if modified <= limit:
                    continue
            if isinstance(item.exclude_from_nav, bool):
                if item.exclude_from_nav:
                    continue
            else:
                if item.exclude_from_nav():
                    continue
            actions = []
            note = INote(item)
            if check_perm(permissions.ModifyPortalContent, item):
                if note.review_state == 'private':
                    actions.append(
                        dict(content=self.context.translate(PMF('Publish')),
                             title="",
                             class_='publish',
                             url=item.absolute_url() +
                             '/content_status_modify?workflow_action=publish'))
        # alternatively use a popup with the form from /content_status_history

                actions.append(
                    dict(content=self.context.translate(_('Color')),
                         title=self.context.translate(_("Change color")),
                         class_='change_color',
                         url=item.absolute_url() + '/change_color'))
                actions.append(
                    dict(content=self.context.translate(PMF('Edit')),
                         title='',
                         class_='edit',
                         url=item.absolute_url() + '/edit'))

            if check_perm(permissions.DeleteObjects, item):
                delete_url = item.absolute_url() \
                    + '/delete_confirmation'
                actions.append(
                    dict(content=self.context.translate(PMF('Delete')),
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
                are_you_sure = self.context.translate(_('Are you sure'))
                notedata.update(dict(are_you_sure=are_you_sure))
            retval.append(notedata)
        for (new_note, new_index) in zip(new, list(range(max_zindex + 1,
                                         max_zindex + len(new) + 1))):
            new_note['zIndex'] = new_index
        return json.dumps(retval)

    def contents(self):
        """ Get the contents of the folder/collection.
        """

        context = aq_inner(self.context)
        settings = NoticeboardSettings(context)
        display_types = [x for x in settings.display_types]
        display_types.append(settings.note_type)
        display_types = list(set(display_types))
        if HAS_AT_TOPIC and IATTopic.providedBy(context):
            # handle very old collections
            items = context.queryCatalog(portal_types=display_types)
        elif HAS_AT_COLLECTIONS and IATCollection.providedBy(context):
            # handle AT collections
            items = context.results(batch=False, brains=False)
        elif ICollection.providedBy(context):
            # handle DX collections
            items = context.results(batch=False, brains=False)

        else:
            # handle folders
            items = context.getFolderContents(
                full_objects=True,
                contentFilter={
                    "portal_type": display_types,
                    "sort_on": "sortable_title"})
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
        if not hide_after:
            self.contents = ""
            return self.index()
        limit = datetime.now() - timedelta(days=hide_after)
        for item in items:
            if hide_after:
                # ignore items that are newer than the limit
                modified = item.modified().utcdatetime()
                if modified >= limit:
                    continue
            notes.append(item)
        self.contents = notes
        return self.index()


# missing translations
dummy = _("Are you sure")
