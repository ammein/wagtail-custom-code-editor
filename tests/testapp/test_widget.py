from django.test import TestCase
from wagtail_custom_code_editor.widgets import CustomCodeEditorWidget


class WidgetTestCase(TestCase):
    @staticmethod
    def _get_init_options(**kwargs):
        options = {
            "mode": "html",
            "theme": "monokai"
        }

        if kwargs:
            options.update(kwargs)

        return options

    def _get_widget(self):
        data = self._get_init_options()
        return CustomCodeEditorWidget(**data)

    def test_default_widget(self):
        widget = CustomCodeEditorWidget()

        self.assertEqual(widget.mode, "html")
        self.assertEqual(widget.theme, "chrome")

    def test_widget_options(self):
        from wagtail_custom_code_editor.settings import wagtail_custom_code_editor_settings
        data = self._get_init_options()
        widget = CustomCodeEditorWidget(**data)

        self.assertEqual(widget.mode, data['mode'])
        self.assertEqual(widget.theme, data['theme'])
        self.assertEqual(widget.options, getattr(wagtail_custom_code_editor_settings, "OPTIONS_TYPES"))
        self.assertEqual(widget.modes, getattr(wagtail_custom_code_editor_settings, "MODES"))

    def test_change_modes(self):
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

        for mode in widget.modes:
            if mode["name"] == "html":
                self.assertEqual(mode["snippet"], data["modes"][0]["snippet"])
                self.assertEqual(mode["title"], data["modes"][0]["title"])
