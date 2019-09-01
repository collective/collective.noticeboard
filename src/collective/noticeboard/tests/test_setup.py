# -*- coding: utf-8 -*-
import unittest

from collective.noticeboard.testing import \
    COLLECTIVENOTICEBOARD_INTEGRATION_TESTING

from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, setRoles, login


class CollectiveNoticeboardClassTest(unittest.TestCase):

    layer = COLLECTIVENOTICEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.types = self.portal.portal_types

    def test_rolemap(self):
        permission = "collective.noticeboard: manage noticeboards"
        self.failUnless(
            self.portal.permission_settings(permission)[0]['acquire'] ==
            '')
        roles = [
            item['name'] for item in self.portal.rolesOfPermission(
                permission
            ) if item['selected'] == 'SELECTED'
        ]
        roles.sort()
        self.assertEqual(
            roles,
            [
                'Manager',
                'Owner',
                'Site Administrator',
            ]
        )

    def test_view_methods(self):
        portal_types = getattr(self.portal, 'portal_types')
        self.assertIn('noticeboardview', portal_types['Folder'].view_methods)
        self.assertIn(
            'noticeboardview', portal_types['Collection'].view_methods)
        self.assertIn(
            'noticeboardview', portal_types['Plone Site'].view_methods)
