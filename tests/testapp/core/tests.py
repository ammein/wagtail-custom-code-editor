from wagtail.test.utils import WagtailPageTestCase
from wagtail.test.utils.page_tests import WagtailPageTests
from wagtail.models import Page, Site

from .models import CustomCodeEditorPage


class CustomCodeEditorPageTests(WagtailPageTests):
    @classmethod
    def setUpTestData(cls):
        root_page = Page.get_first_root_node()
        Site.objects.create(
            root_page=root_page,
            site_name='testsite',
            is_default_site=True,
            hostname='testhost',
        )
        cls.page = CustomCodeEditorPage(
            title='Test Custom Code Editor Page',
            slug='custom-code-editor-page',
        )
        root_page.add_child(instance=cls.page)

    def test_get(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        self.assertPageIsEditable(self.page, post_data={
            'title': 'Change Title Page',
            'slug': 'change-title-page',
            'code': {
                'code': '@code-here',
                'html': 'html'
            }
        })
