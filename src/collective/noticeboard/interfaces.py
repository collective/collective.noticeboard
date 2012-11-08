#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface, Attribute

from collective.noticeboard import _


class INoticeboard(Interface):
    '''Marker interface for content types that can display a noticeboard
    '''


class INoticeboardSettings(Interface):
    '''Marker interface for content types that can be configured for noticeboards
    '''
    note_type = schema.Choice(
        title=_(u"label_Note_type", default=u"Note type"),
        description=_(u"description_note_type",
            default=u"Select, which content type should be created when one"
            u" adds a note. It is your responsability to check, that the"
            u" content types can actually be created. Check the required"
            u" fields!"),
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        default="News Item")

    create_on_click = schema.Bool(
        title=_(u"label_Create_on_click", default="Create a new note when clicking on the canvas"),
        description=_(u"description_Create_on_click", default="Create a new note when clicking on the canvas."),
        default=False)

    publish_on_creation = schema.Bool(
        title=_(u"label_Publish_on_create", default="Auto-publish on creation"),
        description=_(u"description_Publish_on_create", default="Attempt to publish new items on saving."),
        default=False)

    hide_after_days = schema.Int(
        title=_(u"label_Hide_after_days", default="Hide items after x days"),
        description=_(u"description_Hide_after_days", default="Leave '0' to never hide items."),
        default = 0,
        )

class INote(Interface):
    '''Interface for objects that can be displayed as a note
    '''

    text = Attribute('The text to display')
    image_tag = Attribute('The image tag')
    color = Attribute('Color')
    zIndex = Attribute('zIndex')
    position_x = Attribute('Position X')
    position_y = Attribute('Position Y')
    id_ = Attribute('An identifier to recognize an object again')