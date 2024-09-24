from django.test import SimpleTestCase

from wagtail_custom_code_editor.panels import CustomCodeEditorPanel
from wagtail_custom_code_editor.widgets import CustomCodeEditorWidget


class EditHandlersTestCase(SimpleTestCase):
    def test_init_default(self):
        panel = CustomCodeEditorPanel('code')

        self.assertEqual(panel.ace_options['theme'], 'chrome')
        self.assertEqual(panel.ace_options['mode'], 'html')
        self.assertEqual(panel.ace_options['width'], '100%')
        self.assertEqual(panel.ace_options['height'], '300px')
        self.assertEqual(panel.ace_options['enable_options'], True)
        self.assertEqual(panel.ace_options['enable_modes'], False)

    def test_init_with_values(self):
        panel = CustomCodeEditorPanel('code', mode='glsl', theme='monokai', enable_modes=True)

        self.assertEqual(panel.ace_options['theme'], 'monokai')
        self.assertEqual(panel.ace_options['mode'], 'glsl')
        self.assertEqual(panel.ace_options['width'], '100%')
        self.assertEqual(panel.ace_options['height'], '300px')
        self.assertEqual(panel.ace_options['enable_options'], True)
        self.assertEqual(panel.ace_options['enable_modes'], True)

    def test_clone(self):
        panel = CustomCodeEditorPanel('code', theme='monokai', mode='html')
        clone = panel.clone()

        self.assertEqual(panel.ace_options['theme'], clone.ace_options['theme'])
        self.assertEqual(panel.ace_options['mode'], clone.ace_options['mode'])

    def test_widget_overrides(self):
        panel = CustomCodeEditorPanel('code', theme='monokai', mode='css')
        widget_overrides = panel.get_form_options()

        self.assertIsInstance(widget_overrides['widgets']['code'], CustomCodeEditorWidget)
        self.assertIn('code', widget_overrides['fields'])
