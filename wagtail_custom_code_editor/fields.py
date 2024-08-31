from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail_custom_code_editor.validators import CustomCodeEditorDecoder


class CustomCodeEditorField(models.JSONField):
    description = _("Custom Code Editor")

    def __init__(self, *args, **kwargs):
        kwargs['decoder'] = CustomCodeEditorDecoder
        super().__init__(*args, **kwargs)
