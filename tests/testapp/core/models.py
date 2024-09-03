from django.db import models
from wagtail.admin.panels import MultiFieldPanel
from wagtail.models import Page

from wagtail_custom_code_editor.edit_handlers import CustomCodeEditorPanel
from wagtail_custom_code_editor.fields import CustomCodeEditorField


class CustomCodeEditorPage(Page):
    code = CustomCodeEditorField()
    secondcode = CustomCodeEditorField()

    content_panels = Page.content_panels + [
        CustomCodeEditorPanel('code', mode='html', theme='monokai'),
        MultiFieldPanel([
            CustomCodeEditorPanel('secondcode', mode='html', theme='monokai'),
        ], 'Code (Nested)')
    ]
