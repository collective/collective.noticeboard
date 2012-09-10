#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute


class INoticeboard(Interface):
    '''Marker interface for content types that can display a noticeboard
    '''


class INoticeboardSettings(Interface):
    '''Marker interface for content types that can be configured for noticeboards
    '''


class INote(Interface):
    '''Interface for objects that can be displayed as a note
    '''

    text = Attribute('The text to display')
    image_url = Attribute('The image link')
    position_x = Attribute('Position X')
    position_y = Attribute('Position Y')
    id_ = Attribute('An identifier to recognize an object again')


class INoteMarker(Interface):
    '''
    '''
