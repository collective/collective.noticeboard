#!/usr/bin/python
# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations

ANNOTATION_KEY = 'collective.noticeboard'


class BaseNoteAdapter(object):
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


class ArchetypesNoteAdapter(BaseNoteAdapter):

    @property
    def title(self):
        return self.context.Title()

    @property
    def description(self):
        return self.context.Description()

    @property
    def text(self):
        return self.context.id
        text = getattr(self.context, 'getText')
        if text:
            return text()

    @property
    def image_url(self):
        if getattr(self.context, 'getImage', None):
            scale = "mini"
            url = self.context.absolute_url() + "/@@images/" + scale
            return url
        return False


class DexterityNoteAdapter(BaseNoteAdapter):

    @property
    def title(self):
        return self.context.title

    @property
    def description(self):
        return self.context.description

    @property
    def text(self):
        text = getattr(self.context, 'text')
        if text:
            return text.render()

    @property
    def image_url(self):
        if getattr(self.context, 'image', None):
            scale = "mini"
            url = self.context.absolute_url() + "/@@images/" + scale
            return url
        return False
