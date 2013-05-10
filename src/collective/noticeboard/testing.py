import doctest

from zope.configuration import xmlconfig

from plone.testing import z2

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting


class CollectiveNoticboardLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import collective.noticeboard
        xmlconfig.file(
            'configure.zcml',
            collective.noticeboard,
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.noticeboard:default')
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory(
            "Folder",
            id="acceptance-test-folder",
            title=u"Test Folder"
        )


COLLECTIVENOTICEBOARD_FIXTURE = CollectiveNoticboardLayer()

COLLECTIVENOTICEBOARD_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVENOTICEBOARD_FIXTURE,),
    name="CollectiveNoticboardLayer:Integration")
COLLECTIVENOTICEBOARD_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVENOTICEBOARD_FIXTURE,),
    name="CollectiveNoticboardLayer:Functional")
COLLECTIVENOTICEBOARD_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(COLLECTIVENOTICEBOARD_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectiveNoticboardLayer:Acceptance")

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
