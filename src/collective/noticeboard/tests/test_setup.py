# -*- coding: utf-8 -*-
import unittest2 as unittest

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

    def test_css_registered(self):
        cssreg = getattr(self.portal, 'portal_css')
        stylesheets_ids = cssreg.getResourceIds()
        self.failUnless(
            '++resource++collective.noticeboard/noticeboard.css'
            in stylesheets_ids)

    def test_js_registered(self):
        jsreg = getattr(self.portal, 'portal_javascripts')
        script_ids = jsreg.getResourceIds()
        self.failUnless(
            '++resource++collective.noticeboard/noticeboard.js' in script_ids)
        self.failUnless(
            '++resource++collective.noticeboard/mustache.js' in script_ids)
        self.failUnless(
            '++resource++collective.noticeboard/z3cform_widget_code_copy.js'
            in script_ids)

    def test_dependencies_installed(self):
        portal_setup = getattr(self.portal, 'portal_setup')
        self.failIf(portal_setup.getLastVersionForProfile(
            'collective.js.underscore:default') == 'unknown')
        self.failIf(portal_setup.getLastVersionForProfile(
            'collective.js.backbone:default') == 'unknown')
        self.failIf(portal_setup.getLastVersionForProfile(
            'collective.js.jqueryui:default') == 'unknown')

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
        self.assertIn('noticeboardview', portal_types['Topic'].view_methods)
        self.assertIn('noticeboardview',
            portal_types['Collection'].view_methods)
        self.assertIn('noticeboardview',
            portal_types['Plone Site'].view_methods)
