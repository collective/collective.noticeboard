#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.component import adapts, getMultiAdapter
from zope.interface import implements
from zope.publisher.interfaces.browser import IBrowserRequest, \
    IBrowserPublisher
from ZPublisher.BaseRequest import DefaultPublishTraverse

from collective.noticeboard.interfaces import INoticeboard, INote


class BoardTraverser(object):

    '''Catches PUT Requests'''

    adapts(INoticeboard, IBrowserRequest)
    implements(IBrowserPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        return (self.context, ('index_html', ))

    def publishTraverse(self, request, name):
        if name == 'noticeboardnotes':
            #import pdb;pdb.set_trace()
            pass
        if name == 'noticeboardnotes' and not request.URL.endswith('noticeboardnotes'):
            if self.request.method == 'PUT':
                return PUTTraverser(self.context, self.request)
            if self.request.method == 'GET':
                return GETTraverser(self.context, self.request)
        return DefaultPublishTraverse(self.context,
                self.request).publishTraverse(self.request, name)


class PUTTraverser(object):

    '''Injects the right browser views for put requests '''

    adapts(INoticeboard, IBrowserRequest)
    implements(IBrowserPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        return (self.context, ('index_html', ))

    def publishTraverse(self, request, name):
        return getMultiAdapter((self.context[name], self.request),
                               name='PUT')


class GETTraverser(object):

    '''Injects the right browser views for GET requests '''

    adapts(INoticeboard, IBrowserRequest)
    implements(IBrowserPublisher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        return (self.context, ('index_html', ))

    def publishTraverse(self, request, name):
        return getMultiAdapter((self.context[name], self.request),
                               name='GET')

