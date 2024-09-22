import json
import re
from django.test import TestCase, override_settings

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

    def test_change_options_as_string(self):
        from wagtail_custom_code_editor.settings import wagtail_custom_code_editor_settings
        dummy_options = json.dumps(
            dict(readOnly=True, cursorStyle="smooth", printMarginColumn=100, showFoldWidgets=True, printMargin=50))
        data = self._get_init_options()
        data.update({
            "options": dummy_options
        })

        widget = CustomCodeEditorWidget(**data)

        self.assertNotEqual(widget.options, getattr(wagtail_custom_code_editor_settings, "OPTIONS_TYPES"))

        for option in widget.options:
            if option["name"] in json.loads(dummy_options):
                self.assertEqual(option["defaultValue"], json.loads(dummy_options)[option["name"]])

    def test_change_options_as_object(self):
        from wagtail_custom_code_editor.settings import wagtail_custom_code_editor_settings
        dummy_options = dict(readOnly=True, cursorStyle="smooth", printMarginColumn=100, showFoldWidgets=True,
                             printMargin=50)
        data = self._get_init_options()
        data.update({
            "options": dummy_options
        })

        widget = CustomCodeEditorWidget(**data)

        self.assertNotEqual(widget.options, getattr(wagtail_custom_code_editor_settings, "OPTIONS_TYPES"))

        for option in widget.options:
            if option["name"] in dummy_options:
                self.assertEqual(option["defaultValue"], dummy_options[option["name"]])

    def test_check_static_modes(self):
        from django.contrib.staticfiles import finders
        data = self._get_init_options()
        data.update({
            "enable_modes": True
        })
        widget = CustomCodeEditorWidget(**data)
        modes = [d['name'] for d in widget.modes]
        print("Total default modes: %s" % len(modes))
        print(modes)

        total_checked_mode = 0

        for media in widget.media._js:
            valid = re.search(r'(?=mode-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)

                getMode = re.search(r'((?!-)\w)*$', valid.group())
                if getMode.group() in modes:
                    # Make sure that the media is here.
                    self.assertTrue(getMode.group() in modes)
                    resultSnippets = finders.find('wagtail_custom_code_editor/ace/snippets/%s.js' % getMode.group())
                    self.assertTrue(resultSnippets)
                    total_checked_mode += 1

        # Check if push modes is the same as defaultMode
        self.assertEqual(total_checked_mode, len(modes), "Total checked modes not matched with default modes")

    def test_check_static_extra_modes(self):
        from django.contrib.staticfiles import finders
        data = self._get_init_options()
        data.update({
            "enable_modes": True,
            "modes": [{
                "title": "GLSL",
                "name": "glsl",
                "snippet": """#version 300 es
                uniform float time;
                void main() {
                    vec4 color = vec4(vec3(0.), 1.);
                    gl_FragColor = color;
                }"""
            }]
        })

        widget = CustomCodeEditorWidget(**data)
        modes = [d['name'] for d in widget.modes]
        print("Total extra modes: %s" % len(modes))
        print(modes)

        total_checked_mode = 0

        for media in widget.media._js:
            valid = re.search(r'(?=mode-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)

                getMode = re.search(r'((?!-)\w)*$', valid.group())
                if getMode.group() in modes:
                    # Make sure that the mode is here.
                    self.assertTrue(getMode.group() in modes)
                    resultSnippets = finders.find('wagtail_custom_code_editor/ace/snippets/%s.js' % getMode.group())
                    self.assertTrue(resultSnippets)
                    total_checked_mode += 1

        # Check if push modes is the same as defaultMode
        self.assertEqual(total_checked_mode, len(modes), "Total checked modes not matched with default modes")

    @override_settings(WAGTAIL_CUSTOM_CODE_EDITOR={
        "MODES": [{
                "title": "GLSL",
                "name": "glsl",
                "snippet": """#version 300 es
                uniform float time;
                void main() {
                    vec4 color = vec4(vec3(0.), 1.);
                    gl_FragColor = color;
                }"""
            }]
    })
    def test_check_static_settings_modes(self):
        from django.contrib.staticfiles import finders
        from wagtail_custom_code_editor.settings import wagtail_custom_code_editor_settings

        data = {
            "mode": "glsl",
            "theme": "monokai",
            "enable_modes": True
        }

        widget = CustomCodeEditorWidget(**data)
        modes = [d['name'] for d in widget.modes]

        print("Total custom modes: %s" % len(modes))
        print(modes)

        total_checked_mode = 0

        # Check that default OPTIONS_TYPES is still there
        self.assertListEqual(widget.options, getattr(wagtail_custom_code_editor_settings, "OPTIONS_TYPES"))

        for media in widget.media._js:
            valid = re.search(r'(?=mode-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)

                getMode = re.search(r'((?!-)\w)*$', valid.group())
                # Make sure that the mode is here.
                self.assertTrue(getMode.group() in modes)
                resultSnippets = finders.find('wagtail_custom_code_editor/ace/snippets/%s.js' % getMode.group())
                self.assertTrue(resultSnippets)
                total_checked_mode += 1

        # Check if push modes is the same as defaultMode. Must always strict to 1 value
        self.assertEqual(total_checked_mode, 1, "Total checked modes not matched with default modes")

    def test_check_options_enable_modes_is_false(self):
        from django.contrib.staticfiles import finders
        data = self._get_init_options()

        widget = CustomCodeEditorWidget(**data)

        total_checked_mode = 0

        for media in widget.media._js:
            valid = re.search(r'(?=mode-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)

                getMode = re.search(r'((?!-)\w)*$', valid.group())

                self.assertTrue(getMode.group() == "html")
                resultSnippets = finders.find('wagtail_custom_code_editor/ace/snippets/%s.js' % getMode.group())
                self.assertTrue(resultSnippets)
                total_checked_mode += 1

        # Check if push modes is the same as defaultMode
        self.assertEqual(total_checked_mode, 1, f"Total checked modes not strictly matched to one mode: {widget.mode}")

    def test_check_static_extension(self):
        from django.contrib.staticfiles import finders
        from wagtail_custom_code_editor.files import EXTENSIONS
        data = self._get_init_options()

        widget = CustomCodeEditorWidget(**data)

        print("Total default extensions: %s" % len(EXTENSIONS))
        print(EXTENSIONS)

        total_checked_extensions = 0

        for media in widget.media._js:
            valid = re.search(r'(?=ext-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)

                if valid.group() + ".js" in EXTENSIONS:
                    # Make sure that the media is here.
                    self.assertTrue(valid.group() + ".js" in EXTENSIONS)
                    total_checked_extensions += 1

        # Check if push extensions is the same as default extensions
        self.assertEqual(total_checked_extensions, len(EXTENSIONS))

    def test_check_static_custom_extension(self):
        from django.contrib.staticfiles import finders
        from wagtail_custom_code_editor.files import EXTENSIONS
        custom_extensions = ["code_lens", "keybinding_menu"]
        data = self._get_init_options()
        data.update({
            "extensions": custom_extensions
        })

        widget = CustomCodeEditorWidget(**data)

        print("Total custom extensions: %s" % len(custom_extensions))
        print(custom_extensions)

        total_checked_extensions = 0

        for media in widget.media._js:
            valid = re.search(r'(?=ext-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)

                getExtension = re.search(r'((?!-)\w)*$', valid.group())

                if getExtension.group() in custom_extensions:
                    # Make sure that the media is here.
                    self.assertTrue(getExtension.group() in custom_extensions)
                    total_checked_extensions += 1

        # Check if push custom extensions is not the same as default extensions
        self.assertNotEqual(total_checked_extensions, len(EXTENSIONS))

    def test_check_static_theme(self):
        from django.contrib.staticfiles import finders
        data = self._get_init_options()

        widget = CustomCodeEditorWidget(**data)

        total_checked_themes = 0

        for media in widget.media._js:
            valid = re.search(r'(?=theme-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)
                self.assertTrue(valid.group() == "theme-" + widget.theme)
                total_checked_themes += 1

        # Check if push theme is strictly equal to 1 theme
        self.assertEqual(total_checked_themes, 1)

    def test_check_static_keybinding(self):
        from django.contrib.staticfiles import finders
        data = self._get_init_options()
        data.update({
            "keybinding": "emacs"
        })
        widget = CustomCodeEditorWidget(**data)

        total_checked_keybinding = 0

        for media in widget.media._js:
            valid = re.search(r'(?=keybinding-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)
                self.assertTrue(valid.group() == "keybinding-" + widget.keybinding)
                total_checked_keybinding += 1

        # Check if push theme is strictly equal to 1 theme
        self.assertEqual(total_checked_keybinding, 1)

    def test_check_static_worker(self):
        from django.contrib.staticfiles import finders
        from wagtail_custom_code_editor.files import WORKERS
        data = self._get_init_options()

        widget = CustomCodeEditorWidget(**data)
        modes = [d['name'] for d in widget.modes]

        print("Total default workers: %s" % len(WORKERS))
        print(WORKERS)

        # Check if useworker is True by default
        self.assertTrue(widget.useworker)

        for media in widget.media._js:
            valid = re.search(r'(?=worker-).*(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/ace/%s.js' % valid.group())
                self.assertTrue(result)

                getWorker = re.search(r'((?!-)\w)*$', valid.group())

                # Check if workers matched with default static workers
                self.assertTrue(valid.group() + ".js" in WORKERS)

                if getWorker.group() in modes:
                    # Make sure that worker is matches modes options
                    self.assertTrue(getWorker.group() in modes)

    def test_if_widget_use_as_django_admin(self):
        from django.contrib.staticfiles import finders
        data = self._get_init_options()
        data.update({
            "django_admin": True
        })
        widget = CustomCodeEditorWidget(**data)

        total_checked_js = 0

        for media in widget.media._js:
            valid = re.search(r'custom-code-editor-controller(?=.js)', media)
            if valid:
                # Make sure static files is pushed
                result = finders.find('wagtail_custom_code_editor/js/%s.js' % valid.group())
                self.assertFalse(result)
                self.assertFalse(valid.group() == "custom-code-editor-controller")
                total_checked_js += 1

        # Check if push asset is strictly equal to 0 on custom-code-editor-controller javascript file
        self.assertEqual(total_checked_js, 0)
