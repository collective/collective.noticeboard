from AccessControl import Unauthorized
from StringIO import StringIO
from collective.noticeboard.testing import \
    COLLECTIVENOTICEBOARD_INTEGRATION_TESTING
from collective.noticeboard.tests.utils import getData
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
import json
import unittest2 as unittest


class BrowserTests(unittest.TestCase):

    layer = COLLECTIVENOTICEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        login(self.portal, 'admin')
        self.portal.invokeFactory("News Item", "news",
            image=getData('../resources/no.png'))
        login(self.portal, TEST_USER_NAME)
        self.news = self.portal['news']

    def test_check_permission_on_edit(self):
        setRoles(self.portal, TEST_USER_ID, [])
        self.assertRaises(Unauthorized, 
            self.portal.news.restrictedTraverse, '@@json')

        setRoles(self.portal, TEST_USER_ID, ['Reader'])
        view = self.portal.news.restrictedTraverse('@@json')
        view.request.stdin = StringIO(json.dumps({
            'position_x': 1,
            'position_y': 2,
            'height': 3,
            'width': 4,
            'color': 5,
            'zIndex': 6}))
        
        self.assertRaises(Unauthorized, view.put, self.portal.news)
        
        setRoles(self.portal, TEST_USER_ID, ['Editor'])
        self.assertTrue(view.put(self.portal.news))
