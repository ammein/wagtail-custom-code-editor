from __future__ import annotations
from django import forms
from django.utils.translation.template import block_re
from wagtail.blocks import FieldBlock
from django.utils.translation import gettext_lazy as _
from .types import ButtonConfig
from .validators import CustomCodeEditorDecoder
from .widgets import CustomCodeEditorWidget


class CustomCodeEditorBlock(FieldBlock):
    def __init__(
            self,
            required=True,
            help_text: str = None,
            disabled=False,
            label=_('Custom Code Editor'),
            mode=None,
            theme=None,
            width="100%",
            height="300px",
            font_size=None,
            keybinding=None,
            useworker=True,
            extensions=None,
            enable_options=True,
            enable_modes=False,
            dropdown_config: ButtonConfig = None,
            read_only_config: ButtonConfig = None,
            options=None,
            modes=None,
            attrs=None,
            **kwargs,
    ):
        self._ace_options = {
            "mode": mode,
            "theme": theme,
            "width": width,
            "height": height,
            "font_size": font_size,
            "keybinding": keybinding,
            "useworker": useworker,
            "extensions": extensions,
            "enable_options": enable_options,
            "enable_modes": enable_modes,
            "dropdown_config": dropdown_config,
            "read_only_config": read_only_config,
            "options": options,
            "modes": modes,
            "attrs": attrs,
            "block": True
        }
        self.field = forms.JSONField(widget=CustomCodeEditorWidget(**self._ace_options), help_text=help_text, required=required, decoder=CustomCodeEditorDecoder, disabled=disabled, label=label)
        super().__init__(**kwargs)

    class Meta:
        icon = 'code'
