#!/usr/bin/python
# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute


class INoticeboard(Interface):

    '''
    Marker interface for content types that can display a noticeboard
    '''


class INoticeboardSettings(Interface):

    '''
    Marker interface for content types that can be configured for noticeboards
    '''


class INote(Interface):
    '''
    Interface for objects that can be displayed as a note
    '''
    text = Attribute()
    image_url = Attribute()
    position_x = Attribute()
    position_y = Attribute()