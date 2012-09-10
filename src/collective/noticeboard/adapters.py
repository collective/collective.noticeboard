#!/usr/bin/python
# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations

ANNOTATION_KEY = 'collective.noticeboard'


class NewsAdapter(object):

    def __init__(self, context):
        self.context = context
        try:
            self.annotations = \
                IAnnotations(self.context)[ANNOTATION_KEY]
        except KeyError:
            self.annotations = \
                IAnnotations(self.context)[ANNOTATION_KEY] = \
                PersistentDict()

    @property
    def text(self):
        return 'Example'

    @property
    def image_url(self):
        return 'http://www.ccc.de'

    @property
    def position_x(self):
        return self.annotations.get('position_x', 0)

    @position_x.setter
    def position_x(self, value):
        self.annotations['position_x'] = int(value)

    @property
    def position_y(self):
        return self.annotations.get('position_y', 0)

    @position_y.setter
    def position_y(self, value):
        self.annotations['position_y'] = int(value)

    @property
    def id_(self):
        return self.context.id
