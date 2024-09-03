from __future__ import unicode_literals, annotations

import glob
import re
import json
from typing import Dict, List, Any
from django.utils.functional import cached_property
from django.forms import Media, widgets
from wagtail.widget_adapters import WidgetAdapter
from wagtail.telepath import register
from .settings import wagtail_custom_code_editor_settings
from .types import DropdownConfig
from .files import (
    EXTENSIONS,
    MODES,
    WORKERS
)


class CustomCodeEditorWidget(widgets.Widget):
    template_name = 'code.html'

    def __init__(
            self,
            mode="html",
            theme="chrome",
            width="100%",
            height="300px",
            font_size=None,
            keybinding=None,
            useworker=True,
            extensions=None,
            enable_options=True,
            enable_modes=True,
            dropdown_config=None,
            options=None,
            modes=None,
            attrs=None
    ):
        self.mode: str = mode
        self.theme: str = theme
        self.width: str = width
        self.height: str = height
        self.font_size: str = font_size
        self.keybinding: str = keybinding
        self.useworker: bool = useworker
        self.extensions: str | List = extensions
        self.enable_options: bool = enable_options
        self.enable_modes: bool = enable_modes
        self.dropdown_config: DropdownConfig = dropdown_config or {}

        options = json.loads(options) if isinstance(options, dict) else options

        # Merge by key 'name' matches the value of options
        self.options: Dict[str, Any] = {d['name']: d for d in
                                        getattr(wagtail_custom_code_editor_settings, "OPTIONS_TYPES") + options} if bool(
            options) is not False else getattr(wagtail_custom_code_editor_settings, "OPTIONS_TYPES")

        # Merge by key 'name' matches the value of modes
        self.modes: List[Dict[str, str]] = list(
            {d['name']: d for d in getattr(wagtail_custom_code_editor_settings, "MODES") + modes}.values()) if modes is not None else getattr(wagtail_custom_code_editor_settings, "MODES")

        # See if mode not available in modes
        if len([d for d in self.modes if d['name'] == self.mode]) == 0:
            self.modes.append({
                "name": self.mode,
                "title": self.mode.capitalize(),
                "snippet": "@code-here"
            })

        super(CustomCodeEditorWidget, self).__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['width'] = self.width
        context['widget']['height'] = self.height
        context['widget']['font_size'] = self.font_size
        context['widget']['enable_modes'] = bool(self.enable_modes)
        context['widget']['enable_options'] = bool(self.enable_options)
        context['widget']['options'] = self.options
        context['widget']['modes'] = self.modes
        return context

    @cached_property
    def media(self):
        js = [
            "wagtail_custom_code_editor/ace/ace.js",
            "wagtail_custom_code_editor/js/custom-code-editor-controller.js",
            "wagtail_custom_code_editor/js/custom-code-editor.js",
            "wagtail_custom_code_editor/clipboard/clipboard.min.js",
        ]

        save_modes = []

        # For Mode Files
        for modes in self.modes:
            for key, val in modes.items():
                if key == "name":
                    js.append("wagtail_custom_code_editor/ace/mode-%s.js" % val)
                    save_modes.append(val)

        # For Theme Files
        if self.theme:
            js.append("wagtail_custom_code_editor/ace/theme-%s.js" % self.theme)

        # For Keybinding
        if self.keybinding:
            js.append("wagtail_custom_code_editor/ace/keybinding-%s.js" % self.keybinding)

        # For EXT Files
        if self.extensions:
            if isinstance(self.extensions, str):
                js.append(self.extensions)
            else:
                for extension in self.extensions:
                    js.append(extension)
        else:
            # Upload all extensions by default
            for ext in EXTENSIONS:
                js.append("wagtail_custom_code_editor/ace/%s" % ext)

        # For worker if available
        if self.useworker:
            for worker in WORKERS:
                valid = re.search(r'(?=worker-).*(?=.js)', worker)
                if valid:
                    worker_val = re.search(r'(?!worker-)\w+(?!.js)$', valid.group())
                    if worker_val and worker_val.group() in save_modes:
                        js.append("wagtail_custom_code_editor/ace/%s" % worker)

        css = {"screen": ["wagtail_custom_code_editor/css/code.css"]}

        return Media(js=js, css=css)

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['data-controller'] = "custom-code-editor"
        attrs['data-custom-code-editor-mode-value'] = self.mode
        attrs['data-custom-code-editor-theme-value'] = self.theme
        attrs['data-custom-code-editor-modes-value'] = json.dumps(self.modes)
        attrs['data-custom-code-editor-options-value'] = json.dumps(self.options)
        attrs['data-custom-code-editor-dropdown-config-value'] = json.dumps(self.dropdown_config)
        return attrs

    def format_value(self, value):
        if value is None or value == 'null':
            return json.dumps({
                "code": None,
                "mode": self.mode
            })

        return value


class CustomCodeEditorAdapter(WidgetAdapter):
    js_constructor = 'wagtail_custom_code_editor.widgets.CustomCodeEditor'

    def js_args(self, widget):
        args = super().js_args(widget)
        ace = {
            'theme': widget.theme,
            'defaultMode': widget.mode,
            'modes': widget.modes,
            'options': widget.options,
            'dropdownConfig': widget.dropdown_config
        }
        return [
            *args,
            ace,
        ]

    class Media:
        js = ['wagtail_custom_code_editor/js/custom-code-editor-block-widget.js']


register(CustomCodeEditorAdapter(), CustomCodeEditorWidget)
