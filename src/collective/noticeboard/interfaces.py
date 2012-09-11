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
        default="basic")


class INote(Interface):
    '''Interface for objects that can be displayed as a note
    '''

    text = Attribute('The text to display')
    image_tag = Attribute('The image tag')
    position_x = Attribute('Position X')
    position_y = Attribute('Position Y')
    id_ = Attribute('An identifier to recognize an object again')


class INoteMarker(Interface):
    '''
    '''
