from django.utils.html import format_html
from .settings import wagtail_custom_code_editor_settings
from django.utils.safestring import mark_safe

from wagtail import hooks


@hooks.register('insert_editor_js')
def editor_js():
    return mark_safe(format_html('<script src="{}"></script>', wagtail_custom_code_editor_settings.EMMET_URL))
