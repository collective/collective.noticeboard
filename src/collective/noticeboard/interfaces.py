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
        title=_(u"label_Note_type", default=u"Default type for notes"),
        description=_(u"description_note_type",
            default=u"Which content type should be created when adding a note."),
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        default="News Item")

    display_types = schema.List(
        title=_(u"label_Display_types", default=u"Display types"),
        description=_(u"description_display_types",
            default=u"Which content types should be shown on the noticeboard. If the board is a collection this setting will be ignored."),
        value_type=schema.Choice(source="plone.app.vocabularies.ReallyUserFriendlyTypes"),
        default=[])

    create_on_click = schema.Bool(
        title=_(u"label_Create_on_click", default="New note with click on background"),
        description=_(u"description_Create_on_click", default=""),
        default=False)

    publish_on_creation = schema.Bool(
        title=_(u"label_Publish_on_create", default="Publish new items automatically"),
        description=_(u"description_Publish_on_create", default=""),
        default=False)

    hide_after_days = schema.Int(
        title=_(u"label_Hide_after_days", default="Hide old items after a number of days"),
        description=_(u"description_Hide_after_days", default="Items that are older than the number of days entered here are ommitted from the board. Leave 0 to never hide old items."),
        default = 0,
        )

#    available_colors = schema.List(
#        title=_(u"label_Colors", default="Colors"),
#        description=_(u"description_Colors", default="css-classes"),
#        default = [u'yellow', u'blue', u'green', u'pink', u'purple'],
#        )

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