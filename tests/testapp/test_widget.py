from django.test import TestCase, override_settings
from wagtail_custom_code_editor.widgets import CustomCodeEditorWidget

class WidgetTestCase(TestCase):
    def _get_init_options(self, **kwargs):
        options = {
            "mode":"html",
            "theme": "monokai"
        }

        if kwargs:
            options.update(kwargs)

        return options

    def _get_widget(self):
        data = self._get_init_options()
        return CustomCodeEditorWidget(**data)

    def test_widget_options(self):
        from wagtail_custom_code_editor.settings import wagtail_custom_code_editor_settings
        data = self._get_init_options()
        widget = CustomCodeEditorWidget(**data)

        self.assertEqual(widget.mode, data['mode'])
        self.assertEqual(widget.theme, data['theme'])
        self.assertEqual(widget.options, getattr(wagtail_custom_code_editor_settings, "OPTIONS_TYPES"))
        self.assertEqual(widget.modes, getattr(wagtail_custom_code_editor_settings, "MODES"))

    @override_settings()
    def test_change_options(self):
        from wagtail_custom_code_editor.settings import wagtail_custom_code_editor_settings
        data = self._get_init_options()
        data.update({
            "modes": [
                {
                    "title": "HTML",
                    "name": "html",
                    "snippet": "@code-here"
                }
            ]
        })
        widget = CustomCodeEditorWidget(**data)

        self.assertEqual(widget.mode, data['mode'])
        self.assertNotEqual(widget.modes, getattr(wagtail_custom_code_editor_settings, "MODES"))