import unittest2 as unittest

from collective.noticeboard.testing import \
    COLLECTIVENOTICEBOARD_INTEGRATION_TESTING
from collective.noticeboard.tests.utils import getData


class AdapterTests(unittest.TestCase):

    layer = COLLECTIVENOTICEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal.invokeFactory("News Item", "news",
            image=getData('../resources/no.png'))
        self.news = self.portal['news']

    def test_image_tag(self):
        from collective.noticeboard.adapters import image_tag
        retval = image_tag(self.news, 'image')
        self.assertIn('<img src="http://nohost/plone/news/@@images/', retval)
        self.assertIn('.png" alt="news" title="news" height="40" width="40" />',
            retval)

    def test_position_x_default(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('50%', note.position_x)

        self.news.setTitle("Neuer Zettel")
        self.assertEquals('25%', note.position_x)

    def test_position_x_getting_setting(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        note.position_x = '333'
        self.assertEquals('333', note.position_x)

    def test_position_y_default(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('50%', note.position_y)

        self.news.setTitle("Neuer Zettel")
        self.assertEquals('25%', note.position_y)

    def test_position_y_getting_setting(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        note.position_y = '333'
        self.assertEquals('333', note.position_y)

    def test_height_default(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals(150, note.height)

    def test_height_getting_setting(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        note.height = '333'
        self.assertEquals(333, note.height)

    def test_width_default(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals(225, note.width)

    def test_width_getting_setting(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        note.width = '333'
        self.assertEquals(333, note.width)

    def test_color_default(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('yellow', note.color)

    def test_color_getting_setting(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        note.color = 'red'
        self.assertEquals('red', note.color)

    def test_zIndex_default(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('top', note.zIndex)

    def test_zIndex_getting_setting(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        note.zIndex = '22'
        self.assertEquals('22', note.zIndex)

    def test_id_(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('news', note.id_)

    def test_url(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('http://nohost/plone/news', note.url)

    def test_review_state(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('private', note.review_state)

    def test_creator(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('test_user_1_', note.creator())

    def test_author(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals(
            {'username': 'test-user',
             'description': '',
             'language': '',
             'home_page': '',
             'has_email': False,
             'location': '', 'fullname': ''},
            note.author())

    def test_authorname(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertEquals('test_user_1_', note.authorname())

    def test_modified(self):
        from collective.noticeboard.interfaces import INote
        translation_service = self.portal.translation_service.ulocalized_time
        mod_date = self.news.ModificationDate()
        expected = translation_service(mod_date, False, False, self.portal)
        note = INote(self.news)
        # "May 10, 2013"
        self.assertEquals(expected, note.modified())

    def test_byline(self):
        from collective.noticeboard.interfaces import INote
        translation_service = self.portal.translation_service.ulocalized_time
        note = INote(self.news)
        mod_date = self.news.ModificationDate()
        mod_date = translation_service(mod_date, False, False, self.portal)
        # "May 10, 2013"
        expected = u'%s \u2014 test_user_1_' % mod_date

        self.assertEquals(expected, note.byline)

    def test_jsonable(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        expected_dict = {'description': '',
                         'title': '',
                         'color': 'yellow',
                         'text': '',
                         'portal_type':
                         'news item',
                         'height': 150,
                         'zIndex': 'top',
                         'width': 225,
                         'url': 'http://nohost/plone/news/xx',
                         'position_x': '50%',
                         'position_y': '50%',
                         'review_state':
                         'private',
                         'id': 'news'}
        expected_keys = ['byline',
                         'description',
                         'title',
                         'color',
                         'text',
                         'portal_type',
                         'height',
                         'zIndex',
                         'width',
                         'url',
                         'position_x',
                         'position_y',
                         'review_state',
                         'image_tag',
                         'id']
        retval = note.jsonable
        self.assertEquals(expected_keys, retval.keys())
        retval.pop('byline')
        retval.pop('image_tag')
        self.assertEquals(expected_dict, retval)

    def test_title(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.news.setTitle('testtitle')
        self.assertEquals('testtitle', note.title)

    def test_text(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.news.setText('testtext')
        # Not sure if this is actually a bug...
        self.assertEquals('<p>testtext</p>', note.text)

    def test_description(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.news.setDescription('testdescription')
        self.assertEquals('testdescription', note.description)

    def test_image_tag_from_adapter(self):
        from collective.noticeboard.interfaces import INote
        note = INote(self.news)
        self.assertIn('<img src="http://nohost/plone/news/@@images/',
            note.image_tag)
        self.assertIn('.png" alt="news" title="news" height="40" width="40" />',
            note.image_tag)

