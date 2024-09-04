import json
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
        self.assertContains(response, "Test Custom Code Editor Page")

    def test_post(self):
        self.assertPageIsEditable(self.page, post_data={
            "title": "Custom Code",
            "slug": "custom-code",
            "code": {
                "code": "@code-here",
                "mode": "mode"
            }
        })


class CustomCodeEditorCheckTemplatesPageTests(WagtailPageTests):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(
            root_page=root,
            site_name='testsite',
            is_default_site=True,
            hostname='testhost',
        )
        cls.page = CustomCodeEditorPage(
            title='Test Template Custom Code Editor Page',
            slug='custom-code-editor-page',
            code={
                "code": "@code-here",
                "mode": "html"
            }
        )
        root.add_child(instance=cls.page)

    def test_get(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)
        self.assertPageIsRoutable(self.page)

    def test_check_templates(self):
        response = self.client.get(self.page.url)
        self.assertContains(response, "Test Template Custom Code Editor Page")
        self.assertContains(response, "<pre><code>@code-here</code></pre>")
