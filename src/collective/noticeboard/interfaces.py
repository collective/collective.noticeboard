#!/usr/bin/python
# -*- coding: utf-8 -*-
from zope.interface import Interface


class INoticeboard(Interface):

    '''
    Marker interface for content types that can display a noticeboard
    '''


class INoticeboardSettings(Interface):

    '''
    Marker interface for content types that can be configured for noticeboards
    '''
